## General Knoledge

The event pool is a class that is managing the communication between all threads. Currently we have two of them:
 - UI Thread (main one)
 - Grid Controller

Note that the `Grid Generator` is just referenced in the definition of `Grid Controller`

Threads communicate with eachother through a set of event that will be listed below.
The EventPool class is not called as a thread rather is a shared common memory allocation.

### Event types
 - `GRID_PERMUTATION`: This event is initiated by the UI towards the grid manager to call for a permutation when the player makes a move. The payload looks like this: `{"permutation": tuple<tuple<int>>}` where the tuple represents the two coordinates thar are swapped (permuted).
 - `UI_REFRESH`: This event is used by the Grid Manager to trigger a full UI refresh. The payload looks like this: `{"grid": int[][]}` where grid is the grid. See note on grid
 - `UI_UPDATE`: This event allows the grid manager to make a modification on the UI without calling for a full refresh. As the UI is pretty autonomous, this event only focusses on sprites. The payload looks like this: `{"update_type": int, "coordinates": tuple<int>, "new_gem": int|None}` where `update_type` is either 0 for deletion or 1 for a new sprite. `new_gem` is only used when `update_type` is equal to one and it corresponds to the type of the gem taking place at the coordinates. See note on grid for the gem numeration
 - ~~`UI_ACTION`: Useless and deprecated~~
 - `SCORE_UPDATE`: When the score updates, this event is called from the Grid Manager to the UI. The payload looks like this: `{"score": int}` with score being very originally the score.
 - `GEN_TRIGGER`: This event is called by the UI towards the Grid manager, asking it to call for a grid generation. The payload contains the size. The payload looks like this: `{"grid_size": tuple<int>}` where the grid\_size is expressed in the usual coordinates expression

#### Note on grid:

The grid is represented by a 2d array of integer. Each integer represents a gem starting from 1. 0 or None is the absence of gem.
The coordinates, if not specified are stored in an integer tuple (noted `tuple<int>`) representing `(x, y)`, where `(0, 0)` is the top left corner and x is on the horizontal scale and y is on the vertical one.


## Animation

animation_id:
 - 10x -> deletion of gem x
 - 2xy -> x at the bottom, y at the top
 - 30x -> x is appearing

Note: gem id 0 is empty

Done:
 - deletion animation in __routine
 - translation in tick_gravitee
