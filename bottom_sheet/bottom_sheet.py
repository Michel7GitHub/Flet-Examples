
# Draggable (GestureDetector) Bottom Sheet

import flet as ft
from utils.my_map import MyMap
from utils.my_bottomsheet import MyBottomSheet

def main(page: ft.Page):
    page.padding=0

    text = ft.Text("Hi There", size=40)
    desc = ft.Text("Where does it come from? Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of \"de Finibus Bonorum et Malorum\" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, \"Lorem ipsum dolor sit amet..\", comes from a line in section 1.10.32. The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from  \"de Finibus Bonorum et Malorum\" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.")

    rl = ft.Container(
        ft.Row(
            wrap=True,
            scroll=ft.ScrollMode.ALWAYS,
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        padding=ft.padding.only(10,20,10,20),
        height = 300, 
        width=page.width,
        bgcolor=ft.Colors.GREY_50
    )

    for i in range(0, 29):
        rl.content.controls.append(
            ft.Container(
                ft.Text(f"RL{i}", size=24, key=str(i)),
                border=ft.border.all(1, 'grey300'),
                border_radius=12,
                height=90,
                width=140,
                alignment=ft.alignment.center,
                bgcolor='white',
                margin=ft.margin.only(0,0,0,0)
            )
        )
    
    cl = ft.Container(
        ft.Column(
            wrap=True,
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.only(10,0,10,0),
        height=300,
        bgcolor=ft.Colors.GREY_50
    )
    
    for i in range(0, 30):
        cl.content.controls.append(
            ft.Container(
                ft.Text(f"CL{i}", size=30, key=str(i)),
                border=ft.border.all(1, 'grey300'),
                border_radius=12,
                height=80,
                width=180,
                alignment=ft.alignment.center,
                bgcolor='white'
            )
        )
    
    bs_appbar = ft.Container(
        text,
        padding=ft.padding.only(10,0,10,0),
        alignment=ft.alignment.center        
    )
 
    bs_cont = ft.Container(
        content = ft.Column(
            [
                rl,

                ft.Divider(height=1, thickness=1, color='grey300'),

                cl,

                ft.Divider(height=1, thickness=1, color='grey300'),

                ft.Container(
                    ft.Column(
                        [
                            desc
                        ],
                        #scroll=ft.ScrollMode.ALWAYS
                    ),
                    padding=ft.padding.only(10,0,10,0),
                    alignment=ft.alignment.center
                )
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN
        ),
        expand=True
    )

    def map_handle_tap(e):
        pass

    # Set MAP Container
    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    initial_center = (28.05382, -15.69195)
    initial_zoom = 10
    my_map = MyMap(url_template, initial_center, initial_zoom, map_handle_tap)
    
    my_bs = MyBottomSheet(page, bs_appbar, bs_cont, bs_bgcolor='amber100')
    
    page.add(ft.Stack( [ my_map, my_bs ], expand=True))

ft.app(target=main)
