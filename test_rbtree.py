import pytest

import bm_rbtree


def assert_valid_rbtree(node: bm_rbtree.Node) -> int:
    '''Check that the tree rooted by *node* satisfies the invariants of a
    red-black tree.

    Return the tree's black-height (used for recursively validating sub-trees).
    '''
    match node:
        case None:
            return 1  # Leaves are black.
        case (bm_rbtree.Red(left=bm_rbtree.Red()) |
              bm_rbtree.Red(right=bm_rbtree.Red())):
            assert False, f"children of Red nodes must be Black (got {node})"
        case (bm_rbtree.Node(ge, left=bm_rbtree.Node(le)) |
              bm_rbtree.Node(le, right=bm_rbtree.Node(ge))) if ge < le:
            assert False, f"values must be nondecreasing (got {node})"
    # Nodes all have the same black-depth:
    left_black_depth = assert_valid_rbtree(node.left)
    right_black_depth = assert_valid_rbtree(node.right)
    assert left_black_depth == right_black_depth
    # Return new black-depth so parent can validate:
    return left_black_depth + isinstance(node, bm_rbtree.Black)


@pytest.mark.parametrize("count", range(1, 1 << 8))
def test_rbtree(count: int) -> None:
    _, tree = bm_rbtree.rbtree(count)
    assert_valid_rbtree(tree)
