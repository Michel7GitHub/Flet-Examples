
# Draggable Bottom Sheet (GestureDetector) ... Resizing Container

import flet as ft

class MyBottomSheet(ft.GestureDetector):
    def __init__(self, page, bs_appbar, bs_cont, bs_bgcolor='amber100'):
        super().__init__()

        self.page = page
        self.bs_appbar = bs_appbar
        self.bs_cont = bs_cont

        self.current_orientation = None
        self.current_height = None


        # Handle UPDATE GestureDetector (Drag)
        def on_drag_update(e: ft.DragUpdateEvent):

            print("DRAG UPDATE")

            new_height = self.current_height - e.delta_y

            # Clamp height between min and max snap points
            if self.snap_points[self.current_orientation]['height'][0] <= new_height <= self.snap_points[self.current_orientation]['height'][-1]:
                self.current_height = new_height
                # Set new Height & Animation
                self.content.animate = ft.Animation(0, ft.AnimationCurve.DECELERATE)
                self.content.height = self.current_height
                self.update()


        # Handle END GestureDetector (Drag + Velocity)
        def on_drag_end(e: ft.DragEndEvent):

            print("DRAG END", e.primary_velocity)

            snap_collapse     = self.snap_points[self.current_orientation]['height'][0]
            snap_intermidiate = self.snap_points[self.current_orientation]['height'][1]
            snap_expanded     = self.snap_points[self.current_orientation]['height'][2]

            # Check velocity
            if e.primary_velocity > 2500:       # velocity = 1500, fast push down, then close as much as possible
                self.current_height = self.snap_points[self.current_orientation]['height'][0]
            elif e.primary_velocity < -2500:    # velocity = -1500, fast push up, then open as much as possible
                self.current_height = self.snap_points[self.current_orientation]['height'][-1]

            elif e.primary_velocity > 100:      # velocity = 100, slow push down, then close one level down
                self.current_height = snap_collapse if self.current_height < snap_intermidiate else snap_intermidiate
            elif e.primary_velocity < -100:     # velocity = -100, slow push up,, then open one level up
                self.current_height = snap_expanded if self.current_height > snap_intermidiate else snap_intermidiate

            # For low level velocity, we set Height to nearest SNAP
            else:
                if self.current_height > snap_intermidiate + 150:
                    self.current_height = snap_expanded
                elif self.current_height > snap_intermidiate - 150:
                    self.current_height = snap_intermidiate
                else:
                    self.current_height = snap_collapse

            # Set new Height & Animation
            self.content.animate=ft.Animation(600, ft.AnimationCurve.DECELERATE)
            self.content.height = self.current_height  
            self.update()

    
        self.on_vertical_drag_update = on_drag_update
        self.on_vertical_drag_end = on_drag_end
        self.bottom=0

        self.content = ft.Container(
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

                    self.bs_appbar,
                    self.bs_cont
                ]
            ),
            bgcolor = bs_bgcolor,
            border_radius=ft.border_radius.only(top_left=20, top_right=20),
            height = self.current_height,
            animate=ft.Animation(400, ft.AnimationCurve.DECELERATE), # Animation settings
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=4, color=ft.Colors.BLACK26),
            alignment=ft.alignment.bottom_center
        )


        def resize():
    
            # Orientations Layout : 'H': Horizontal, 'V': Vertical
            #   height : [Collapse, Intermediate, Expanded]
            #   width : gd width
            #   left : gd left position in Stack
            self.snap_points = {
                'H' : { 'height': [ 120, int(page.height * 0.44), int(page.height - 30)],
                        'width': 400,
                        'left'  : 15
                    },
                'V' : { 'height': [ 120, int(page.height * 0.44), int(page.height * 0.9)],
                        'width' : page.width,
                        'left'  : 0
                    }
            }

            # Set default Bottom Sheet height & width
            if page.width > 700 and page.width > page.height :
                self.current_orientation = "H"
                self.current_height = self.snap_points[self.current_orientation]['height'][2]
            else:
                self.current_orientation = "V"
                self.current_height = self.snap_points[self.current_orientation]['height'][1]

            self.content.height = self.current_height
            self.content.width = self.snap_points[self.current_orientation]['width']
            self.bs_cont.width = self.snap_points[self.current_orientation]['width']
            self.left = self.snap_points[self.current_orientation]['left']
            

        def page_on_resize(e):
            resize()
            self.update()

        resize()
        page.on_resized = page_on_resize
