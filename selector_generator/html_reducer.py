from pathlib import Path

from bs4 import BeautifulSoup
from bs4 import Comment
from bs4 import Tag


class HtmlReducerForSelectors:
    """
    Reduces HTML for an LLM whose job is to write an XPath / CSS selector.

    Unlike a "reduce to readable text" reducer, this one:
      - KEEPS real tag structure (so the AI can see nesting / hierarchy)
      - KEEPS attributes that matter for selectors: id, class, name,
        data-*, aria-*, href, type, role
      - DROPS attributes that never matter for selectors: style, on*,
        tracking/analytics junk
      - COLLAPSES repeated sibling elements (e.g. 50 <li class="product">)
        down to the first N, replacing the rest with a single marker
        comment, so the AI still sees the repeating pattern without
        paying token cost for every copy.
    """

    # Tags that never help write a selector / are never a selector target.
    NOISE_TAGS = [
        "script",
        "style",
        "svg",
        "iframe",
        "noscript",
        "link",
        "meta",
        "head",
    ]

    # Attribute names (or prefixes) worth keeping for selector-writing.
    KEEP_ATTR_EXACT = {
        "id",
        "class",
        "name",
        "href",
        "type",
        "role",
        "title",
        "placeholder",
        "value",
        "for",
        "alt",
    }
    KEEP_ATTR_PREFIXES = ("data-", "aria-")

    def __init__(
        self,
        output_dir: str = "logs/html/reduced_html",
        keep_first_n_siblings: int = 3,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.keep_first_n_siblings = keep_first_n_siblings

    def reduce(
        self,
        html_file: Path,
        max_chars: int = 15000,
    ) -> Path:
        html = html_file.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")

        self._remove_noise(soup)
        self._strip_irrelevant_attrs(soup)
        self._collapse_repeated_siblings(soup)

        reduced_html = soup.prettify()

        if len(reduced_html) > max_chars:
            reduced_html = reduced_html[:max_chars]

        output_file = self.output_dir / html_file.name
        output_file.write_text(reduced_html, encoding="utf-8")

        return output_file

    def _remove_noise(self, soup: BeautifulSoup) -> None:
        for tag in soup(self.NOISE_TAGS):
            tag.decompose()

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Drop elements explicitly hidden — never a useful selector target.
        # find_all(True) builds its result list up-front. Decomposing a tag
        # also decomposes (and nulls the .attrs of) all its descendants. If
        # an ancestor earlier in this same list gets decomposed, descendants
        # later in the list are already-decomposed by the time we reach
        # them, so we must skip anything whose .attrs is no longer a dict.
        for tag in soup.find_all(True):
            if not isinstance(tag, Tag) or tag.attrs is None:
                continue
            style_val = tag.get("style") or ""
            style = str(style_val).replace(" ", "")
            if "display:none" in style or tag.get("aria-hidden") == "true":
                tag.decompose()

    def _strip_irrelevant_attrs(self, soup: BeautifulSoup) -> None:
        for tag in soup.find_all(True):
            if not isinstance(tag, Tag):
                continue
            kept = {}
            for attr, val in tag.attrs.items():
                attr_lower = attr.lower()
                if attr_lower in self.KEEP_ATTR_EXACT or attr_lower.startswith(
                    self.KEEP_ATTR_PREFIXES
                ):
                    kept[attr] = val
            tag.attrs = kept

    def _sibling_signature(self, tag: Tag) -> tuple:
        """A signature used to detect 'same kind of element' siblings."""
        classes = tag.get("class")
        class_key = tuple(sorted(classes)) if classes else ()
        return (tag.name, class_key)

    def _collapse_repeated_siblings(self, soup: BeautifulSoup) -> None:
        """
        For every parent in the tree, find runs of consecutive child tags
        that share the same (tag name, class) signature. Keep only the
        first N in each run; replace the remainder with one marker comment
        stating how many were collapsed.
        """
        n = self.keep_first_n_siblings

        # Collect parents first since we'll be mutating children during the
        # walk — operating on a static list avoids skipping/mutating issues.
        all_parents = [p for p in soup.find_all(True) if isinstance(p, Tag)] + [soup]

        for parent in all_parents:
            children = [c for c in parent.children if isinstance(c, Tag)]
            if len(children) <= n:
                continue

            i = 0
            while i < len(children):
                sig = self._sibling_signature(children[i])
                run = [children[i]]
                j = i + 1
                while j < len(children) and self._sibling_signature(children[j]) == sig:
                    run.append(children[j])
                    j += 1

                if len(run) > n:
                    extra = run[n:]
                    collapsed_count = len(extra)
                    marker = Comment(
                        f" ...{collapsed_count} more <{sig[0]}"
                        f"{'.' + '.'.join(sig[1]) if sig[1] else ''}> "
                        f"sibling(s) collapsed... "
                    )
                    extra[0].insert_before(marker)
                    for el in extra:
                        el.decompose()

                i = j

    def get_selector_context(self, html_file: Path, max_chars: int = 50000) -> str:
        """Convenience: returns the reduced HTML as a string instead of a file."""
        out_path = self.reduce(html_file, max_chars=max_chars)
        return out_path.read_text(encoding="utf-8")
