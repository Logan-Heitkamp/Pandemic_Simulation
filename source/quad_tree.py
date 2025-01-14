
class Node:
    def __init__(self, corners: list[list[int]], content: any) -> None:
        self.corners = corners  # tl and br
        self.content = content
        self.quads = []

    def update_quads(self, new_quad: 'Quad') -> None:
        remove_list = []
        old_quads = self.quads.copy()
        old_quads.append(new_quad)

        for idx, this_quad in enumerate(old_quads):
            for that_quad in old_quads[idx + 1:]:
                # if quad is a parent quad of another quad, remove parent quad
                if this_quad == that_quad.parent_quad or this_quad == that_quad:
                    remove_list.append(this_quad)

        # keep all quads not in remove list
        for remove_quad in remove_list:
            old_quads.remove(remove_quad)

        self.quads = old_quads

    # NOTE - only works for nodes of same size. Cases with different sizes are not handled.
    def test_collision(self, collision_test_node: 'Node') -> bool:
        node_tl, node_br = self.corners
        node_tr = (node_br[0], node_tl[1])
        node_bl = (node_tl[0], node_br[1])
        test_tl, test_br = collision_test_node.corners

        # if node_tl in collision_test_node (x-axis)
        if test_tl[0] <= node_tl[0] <= test_br[0]:
            # (y-axis)
            if test_br[1] <= node_tl[1] <= test_tl[1] or test_br[1] <= node_bl[1] <= test_tl[1]:
                return True

        # test if node_br in collision_test_node (x-axis)
        if test_tl[0] <= node_br[0] <= test_br[0]:
            # (y-axis)
            if test_br[1] <= node_br[1] <= test_tl[1] or test_br[1] <= node_tr[1] <= test_tl[1]:
                return True

        # no collision
        return False

    def find_collisions(self) -> list:
        collision_list = []

        for collision_quad in self.quads:
            for collision_node in collision_quad.nodes:
                if collision_node != self:
                    if self.test_collision(collision_node):
                        collision_list.append(collision_node)

        return collision_list

    def __str__(self):
        return f'Node: {self.content}'

    def __repr__(self) -> str:
        return 'Node'


class Quad:
    def __init__(self, tl: tuple[int, int], br: tuple[int, int], node_size: int, parent_quad: 'Quad' = None) -> None:
        self.top_left = tl
        self.bottom_right = br
        self.parent_quad = parent_quad
        self.node_size = node_size

        self.top_left_quad = None
        self.top_right_quad = None
        self.bottom_left_quad = None
        self.bottom_right_quad = None

        self.split = False
        self.nodes = []
        self.node_size = node_size

    def place_node(self, place_node: Node) -> None:
        # add node to list of nodes in this quad
        self.nodes.append(place_node)

        # update node to show which quad it is in
        place_node.update_quads(self)

        # split quad if there are more than 5 nodes in quad
        if not self.split and len(self.nodes) == 6:
            # ensure quads are not smaller than the nodes
            if self.top_left[1] - self.bottom_right[1] > (self.node_size * 2):
                self.split_quad()
        elif self.split:
            self.place_node_in_sub_quad(place_node)

    def split_quad(self) -> None:
        # tag quad as split
        self.split = True

        # define the corners of the new quads
        tl = self.top_left
        br = self.bottom_right
        tm = (((br[0] - tl[0]) // 2) + tl[0], tl[1])
        ml = (tl[0], ((tl[1] - br[1]) // 2) + br[1])
        mm = (tm[0], ml[1])
        mr = (br[0], ml[1])
        bm = (mm[0], br[1])

        # create four sub quads
        self.top_left_quad = Quad(tl, mm, self.node_size, parent_quad=self)
        self.top_right_quad = Quad(tm, mr, self.node_size, parent_quad=self)
        self.bottom_left_quad = Quad(ml, bm, self.node_size, parent_quad=self)
        self.bottom_right_quad = Quad(mm, br, self.node_size, parent_quad=self)

        # place existing nodes in the new quads
        for split_node in self.nodes:
            self.place_node_in_sub_quad(split_node)

    def place_node_in_sub_quad(self, where_place_node: Node) -> None:
        node_top_left = where_place_node.corners[0]
        node_bottom_right = where_place_node.corners[1]

        # if br of node in right half
        if node_bottom_right[0] >= self.top_right_quad.top_left[0]:
            # if tl of node is in top half
            if node_top_left[1] >= self.top_right_quad.bottom_right[1]:
                # place node in tr quad
                self.top_right_quad.place_node(where_place_node)
            # if br of node in bottom half
            if node_bottom_right[1] <= self.bottom_right_quad.top_left[1]:
                # place node in br quad
                self.bottom_right_quad.place_node(where_place_node)

        # if tl of node in left half
        if node_top_left[0] <= self.top_left_quad.bottom_right[0]:
            # if tl of node is in top half
            if node_top_left[1] >= self.top_left_quad.bottom_right[1]:
                # place node in tr quad
                self.top_left_quad.place_node(where_place_node)
            # if br of node in bottom half
            if node_bottom_right[1] <= self.bottom_left_quad.top_left[1]:
                # place node in br quad
                self.bottom_left_quad.place_node(where_place_node)

    def __str__(self) -> str:
        return (f'top_left: {self.top_left}\n'
                f'bottom_right: {self.bottom_right}\n')

    def __repr__(self) -> str:
        return 'Quad'
