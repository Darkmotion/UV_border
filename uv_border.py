"""
Click to select all UV borders edges.
Ctrl + click to select edges and break phong.
Darkmotion 2018
vk.com/darkmotion
"""

import c4d
from c4d import gui
from c4d.utils import Neighbor


def ctrl_hold():
    state = c4d.BaseContainer()
    gui.GetInputEvent(c4d.BFM_INPUT_KEYBOARD, state)
    res = state.GetData(c4d.BFM_INPUT_QUALIFIER) == c4d.QCTRL
    return res


def check_edge(a, b, uv, p_a, p_b):
    a_data = uv.GetSlow(a).values()
    b_data = uv.GetSlow(b).values()
    a_data = a_data[:3] if p_a.IsTriangle() else a_data  # check triangle
    b_data = b_data[:3] if p_b.IsTriangle() else b_data
    counter = 0
    for vec in a_data:
        if vec in b_data:
            counter += 1

    return counter < 2


def main():
    obj = doc.GetActiveObject()
    if not isinstance(obj, c4d.PolygonObject):
        return 0

    uv_tag = obj.GetTag(c4d.Tuvw)
    neigh = Neighbor()
    neigh.Init(obj)
    polys = obj.GetAllPolygons()
    select = c4d.BaseSelect(neigh.GetEdgeCount()-1)

    for ind, poly in enumerate(polys):
        data = neigh.GetPolyInfo(ind)
        for i in range(4):
            n_ind = data['face'][i]
            if data['mark'][i] or i == 2 and poly.c == poly.d:
                continue
            elif n_ind == -1 or check_edge(ind, n_ind, uv_tag, poly, polys[n_ind]):
                select.Select(data['edge'][i])

    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SELECTION, obj)
    obj.SetSelectedEdges(neigh, select, c4d.EDGESELECTIONTYPE_SELECTION)
    if ctrl_hold():
        obj.SetSelectedEdges(neigh, select, c4d.EDGESELECTIONTYPE_PHONG)
        obj.SetPhong(1, 1, 40)
    doc.SetMode(c4d.Medges)


if __name__ == '__main__':
    main()
    c4d.EventAdd()
