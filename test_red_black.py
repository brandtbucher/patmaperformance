import hypothesis

import bm_red_black


def assert_valid_tree(node: bm_red_black.Node | None) -> int:
    """Check that the tree rooted by *node* satisfies the invariants of a
    red-black tree.

    Return the tree's black-height (used for recursively validating sub-trees).
    """
    match node:
        case None:
            # Leaves are black:
            return 1
        case (
            bm_red_black.Red(left=bm_red_black.Red())
            | bm_red_black.Red(right=bm_red_black.Red())
        ):
            assert False, f"children of Red nodes must be Black (got {node})"
        case (
            bm_red_black.Node(ge, left=bm_red_black.Node(le))
            | bm_red_black.Node(le, right=bm_red_black.Node(ge))
        ) if ge < le:
            assert False, f"values must be nondecreasing (got {node})"
    # Nodes all have the same black-depth:
    depth = assert_valid_tree(node.left)
    assert depth == assert_valid_tree(node.right)
    # Return new black-depth so parent can validate:
    return depth + isinstance(node, bm_red_black.Black)


@hypothesis.given(values=hypothesis.infer)
def test_red_black(values: list[int]) -> None:
    hypothesis.assume(1 <= len(values) < 1 << 8)
    root = bm_red_black.Black(values.pop(), None, None)
    for value in values:
        root = root.add(value)
        assert_valid_tree(root)
