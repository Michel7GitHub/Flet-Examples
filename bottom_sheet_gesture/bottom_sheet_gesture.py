
# ??????????????????????????????  ANIMATE.POSITION doesn't work ????????????????????????????????

# Draggable (GestureDetector) Bottom Sheet ... Using STACK TOP Positionning & Resizing Container
#                                              ****************************   ******************
#
#   States: 1. Closed (opacity = 0) default
#           2. Open minimum (gd_top_max ==> page.height - 150 pixels)
#           3. Open middle  (gd_top_mid ==> page.height / 2)
#           4. Open maximum (gd_top_min ==> 150 pixels)
#
#   Moves:  1. High velocity Down ==> Close Bottom Sheet
#           2. Low  velocity Down ==> Close half Bottom Sheet
#           3. High velocity Up ==> Open Bottom Sheet
#           4. Low  velocity Up ==> Open half Bottom Sheet

import flet as ft
from utils.mymap import MyMap

# Container Top-Margin Keeper
#   gd_top_current  = CURRENT GD Top Position   
#   gd_top_min      = MINIMUM GD Top Position
#   gd_top_mid      = MIDDLE GD Top Position  ... None if not enough space
#   gd_top_max      = MAXIMUM GD Top Position
gd_top_current = None                   
gd_top_min = None                                
gd_top_mid = None            
gd_top_max = None

def main(page: ft.Page):
    page.padding=0

    global gd_top_current
    global gd_top_min
    global gd_top_mid
    global gd_top_max


    def on_drag_update(e: ft.DragUpdateEvent):
        global gd_top_current
        
        # Recalculate Margin Top
        gd_top_current = gd_top_current + e.delta_y
        if gd_top_current  > gd_top_max:
            gd_top_current = gd_top_max
        if gd_top_current < gd_top_min:
            gd_top_current = gd_top_min
        
        # Repositionne Gesture Detector (GD) & Resize GD Content
        gd.top = gd_top_current
        gd.update()


    def on_drag_end(e: ft.DragEndEvent):
        global gd_top_current
        
        # Check Y velocity level
        if e.primary_velocity > 1500:       # velocity = 1500, fast push down, then close as much as possible
            gd_top_current = gd_top_max
        elif e.primary_velocity < -1500:    # velocity = -1500, fast push up, then open as much as possible
            gd_top_current = gd_top_min
            
        elif e.primary_velocity > 100:      # velocity = 100, slow push down, then close one level down
            if gd_top_mid != None:
                if gd_top_current > gd_top_mid:
                    gd_top_current = gd_top_max
                else:
                    gd_top_current = gd_top_mid
            else:
                gd_top_current = gd_top_max
        elif e.primary_velocity < -100:     # velocity = -100, slow push up,, then open one level up
            if gd_top_mid != None:
                if gd_top_current < gd_top_mid:
                    gd_top_current = gd_top_min
                else:
                    gd_top_current = gd_top_mid
            else:
                gd_top_current = gd_top_min

        # For low level velocity (150), we set Top to nearest Max|Mid|Min
        else:
            if gd_top_mid != None:
                if gd_top_current > gd_top_mid + 150:
                    gd_top_current = gd_top_max
                elif gd_top_current > gd_top_mid - 150:
                    gd_top_current = gd_top_mid
                else:
                    gd_top_current = gd_top_min
            else:
                if gd_top_current < gd_top_max / 2:
                    gd_top_current = gd_top_min
                else:
                    gd_top_current = gd_top_max


        # Set new value for Height & Top
        gd.top = gd_top_current
        page.update()


    text = ft.Text("Hello toi", size=40)
    desc = ft.Text("Where does it come from? Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of \"de Finibus Bonorum et Malorum\" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, \"Lorem ipsum dolor sit amet..\", comes from a line in section 1.10.32. The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from  \"de Finibus Bonorum et Malorum\" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.")
    
    ct = ft.Container(
        content = ft.Column(
            [
                ft.Row(
                    [ 
                        ft.Container(
                            height=4, 
                            width=50,
                            bgcolor=ft.Colors.GREY_500, 
                            border_radius=ft.border_radius.all(5),
                            margin=ft.margin.only(top=8)
                        ) 
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                text,
                desc
            ],
        ),
        bgcolor = "yellow",
        border_radius=ft.border_radius.only(top_left=20, top_right=20),
        padding=ft.padding.only(10,0,10,0)
    )

    gd = ft.GestureDetector(
        content=ct,
        on_vertical_drag_update=on_drag_update,
        on_vertical_drag_end=on_drag_end,
        drag_interval=10,
        width=390,
        #animate_position=600,
        top = gd_top_current
    )

    def map_handle_tap(e):
        pass

    # Set MAP Container
    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    initial_center = (28.05382, -15.69195)
    initial_zoom = 10
    mp = MyMap(url_template, initial_center, initial_zoom, map_handle_tap)
    
    page.add(ft.Stack( [ mp, gd ], expand=True))


    # Init values depending of Window size
    def page_resized_init():        
        global gd_top_current
        global gd_top_min
        global gd_top_mid
        global gd_top_max
        
        w = page.width
        h = page.height

        if w > 700 and w > h :
            gd_top_min = 10
            gd_top_mid = None
            gd_top_max = h - 120
            gd_top_current = gd_top_min
            ct_width = 390
            ct_margin = ft.margin.only(10,0,10,0)
        else :
            gd_top_min = 90
            gd_top_mid = int(h / 2)
            gd_top_max = h - 120
            gd_top_current = gd_top_mid
            ct_width = w
            ct_margin = ft.margin.only(0,0,0,0)

        gd.top = gd_top_current
        gd.width = ct_width
        ct.height = h - gd_top_min
        ct.margin = ct_margin
        gd.update()

    def page_on_resized(e):
        page_resized_init()
    page.on_resized = page_on_resized
    page_resized_init()

ft.app(target=main)
