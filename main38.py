import pygame as pg
from scripts import game38 as game
import random as rnd

screen_size = (800, 800)
pg.init()
pg.display.set_caption('WumpusWelt')
root = pg.display.set_mode(screen_size)
sprites = game.load_sprites()
fields = []
player = game.Player(fields)
#############################
# choice to see all or not: #
visible = False
#############################

def layout_init():
    global sprites, fields, player, visible
    for x in range(0, 4):
        row =[]
        for y in range(0, 4):
            pos = [
                x * 200,
                y * 200
            ]
            row.append(game.Field(pos, sprites[game.Sprites.empty.value], sprites, player, visible))
            row[-1].draw(root)
            pg.display.update()
        fields.append(row)

def gen_wg():
    global fields
    wumpus = False
    gold = False
    while not wumpus or not gold:
        pos = [rnd.randint(0, 3), rnd.randint(0, 3)]
        if pos != [0, 3]:
            if not fields[pos[0]][pos[1]].pit and not fields[pos[0]][pos[1]].wumpus:
                if wumpus:
                    fields[pos[0]][pos[1]].gold = True
                    gold = True
                else:
                    fields[pos[0]][pos[1]].wumpus = True
                    wumpus = True
    gen_effects()
    return


def gen_effects():
    global fields
    for x, row in enumerate(fields):
        for y, field in enumerate(row):
            if field.wumpus:                        # we add stench around the wumpus
                try:
                    fields[x][y + 1].stench = True
                except IndexError:
                    pass
                try:
                    if not y - 1 < 0:
                        fields[x][y - 1].stench = True
                except IndexError:
                    pass
                try:
                    fields[x + 1][y].stench = True
                except IndexError:
                    pass
                try:
                    if not x - 1 < 0:
                        fields[x - 1][y].stench = True
                except IndexError:
                    pass
            elif field.pit:                        # we add breeze around the pits
                try:
                    fields[x][y + 1].breeze = True
                except IndexError:
                    pass
                try:
                    if not y - 1 < 0:
                        fields[x][y - 1].breeze = True
                except IndexError:
                    pass
                try:
                    fields[x + 1][y].breeze = True
                except IndexError:
                    pass
                try:
                    if not x - 1 < 0:
                        fields[x - 1][y].breeze = True
                except IndexError:
                    pass

def go_draw():
    global fields, root
    for row in fields:
        for field in row:
            field.gen_drawing_sprites()
            root = field.draw(root)

def main():
    global player
    running = True
    changed = True
    layout_init()
    gen_wg()
    player.fields = fields

    while running:
        pg.display.update()
        if changed:
            go_draw()
            changed = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                        changed = player.turn_right()
                        # turn Right
                elif event.key == pg.K_a:
                        changed = player.turn_left()
                        # turn Left
                elif event.key == pg.K_SPACE:
                        player.move()
                        changed = True
                        # move
                elif event.key == pg.K_e:
                        player.pick_up()
                elif event.key == pg.K_f:
                        # shoot an arrow
                        if player.arrow:
                            player.shoot()
                            changed = True
            elif event.type == pg.QUIT:                       # closing the program
                    running = False

if __name__ == '__main__':
    main()
