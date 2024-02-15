from model import *
from typing import List
from car import Car
from map import Map
from math import ceil
from time import sleep

INTERSECTION_WIDTH = Meters(20)


def draw_state(pycasso, cars: List[Car], whole_length: Meters, map: Map):

    # Length of each text character
    DX = pycasso.width / whole_length
    DY = pycasso.height / whole_length
    pycasso.clear()

    for row in map.intersections:
        for intersec in row:
            x = round((intersec.position[0] - INTERSECTION_WIDTH / 2) * DX)
            y = round((intersec.position[1] - INTERSECTION_WIDTH / 2) * DY)

            if intersec.light is None:
                pycasso.fillStyle("rgb(200 100 50)")
            else:
                pycasso.fillStyle("rgb(200 0 0)")

            pycasso.fillRect(
                x,
                y,
                INTERSECTION_WIDTH * DX,
                INTERSECTION_WIDTH * DX,
            )

            if intersec.light is None:
                continue

            if intersec.light.x_light is Lightcolor.Green:
                pycasso.fillStyle("rgb(0 200 0)")
                pycasso.fillRect(
                    x,
                    y + INTERSECTION_WIDTH * DX / 4,
                    INTERSECTION_WIDTH * DX,
                    INTERSECTION_WIDTH * DX - INTERSECTION_WIDTH * DX / 2,
                )
            elif intersec.light.x_light is Lightcolor.Yellow:
                pycasso.fillStyle("rgb(200 200 0)")

                pycasso.fillRect(
                    x,
                    y + INTERSECTION_WIDTH * DY / 4,
                    INTERSECTION_WIDTH * DX,
                    INTERSECTION_WIDTH * DY - INTERSECTION_WIDTH * DY / 2,
                )
            elif intersec.light.y_light is Lightcolor.Green:
                pycasso.fillStyle("rgb(0 200 0)")
                pycasso.fillRect(
                    x + INTERSECTION_WIDTH * DX / 4,
                    y,
                    INTERSECTION_WIDTH * DX - INTERSECTION_WIDTH * DX / 2,
                    INTERSECTION_WIDTH * DY,
                )
            elif intersec.light.y_light is Lightcolor.Yellow:
                pycasso.fillStyle("rgb(200 200 0)")
                pycasso.fillRect(
                    x + INTERSECTION_WIDTH * DX / 4,
                    y,
                    INTERSECTION_WIDTH * DX - INTERSECTION_WIDTH * DX / 2,
                    INTERSECTION_WIDTH * DY,
                )

    for car in cars:
        if car.braking:
            pycasso.fillStyle("rgb(200 10 50)")
        else:
            pycasso.fillStyle("rgb(100 100 254)")

        x = round(car.position[0] * DX)
        y = round(car.position[1] * DY)

        if car.direction == Direction.N or car.direction == Direction.S:
            pycasso.fillRect(
                x - car.length * DX / 2,
                y - car.width * DX / 2,
                car.width * DX,
                car.length * DX,
            )
        else:
            pycasso.fillRect(
                x - car.width * DX / 2,
                y - car.length * DX / 2,
                car.length * DX,
                car.width * DX,
            )

    pycasso.draw()

    sleep(1 / 60)
