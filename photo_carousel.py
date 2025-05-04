import flet as ft

counter = 0

def main(page):

    page.padding=0

    def handle_confirm_dismiss(e: ft.DismissibleDismissEvent):
        global counter
        counter=counter+1 if e.direction == ft.DismissDirection.END_TO_START else counter-1
        dis_column.controls[0] = build_dismiss()
        dis_count.content.value = f"{counter+1} / {len(dis_src)}"
        page.update()

    dis_src = [
        "http://192.168.0.46:8000/medium/000/000/1.jpg",
        "http://192.168.0.46:8000/medium/000/000/2.jpg",
        "http://192.168.0.46:8000/medium/000/000/3.jpg",
        "http://192.168.0.46:8000/medium/000/000/4.jpg",
        "http://192.168.0.46:8000/medium/000/000/5.jpg",
        "http://192.168.0.46:8000/medium/000/000/6.jpg",
        "http://192.168.0.46:8000/medium/000/000/7.jpg",
        "http://192.168.0.46:8000/medium/000/000/8.jpg",
        "http://192.168.0.46:8000/medium/000/000/9.jpg",
        "http://192.168.0.46:8000/medium/000/000/10.jpg",
        "http://192.168.0.46:8000/medium/000/000/11.jpg"
    ]
    
    def build_dismiss():
        global counter

        print("Counter = ", counter)
        
        if counter == len(dis_src):
            counter = 0
        elif counter < 0:
            counter = len(dis_src) - 1


        if len(dis_src) == 1:
            dismiss = ft.Container(
                ft.Image(
                    src=dis_src[0],
                    fit=ft.ImageFit.FIT_WIDTH, width=390
                )
            )
            return dismiss

        elif len(dis_src) == 2:
            if counter == 0:
                (c1, c2, c3) = (0, 1 ,1)
            else:
                (c1, c2, c3) = (1, 0, 0)

        else:
            if counter == 0:
                (c1, c2, c3) = (0, len(dis_src)-1, 1)
            elif counter == len(dis_src) - 1:
                (c1, c2, c3) = (len(dis_src)-1 , len(dis_src)-2, 0)
            else:
                (c1, c2, c3) = (counter, counter-1, counter+1)

        dismiss = ft.Dismissible(
            content=ft.Container(
                ft.Image(
                    src=dis_src[c1],
                    fit=ft.ImageFit.FIT_WIDTH, width=390
                )
            ),
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
            background = ft.Container(
                ft.Image(
                    src=dis_src[c2],
                    fit=ft.ImageFit.FIT_WIDTH, width=390
                )
            ),
            secondary_background = ft.Container(
                ft.Image(
                    src=dis_src[c3],
                    fit=ft.ImageFit.FIT_WIDTH, width=390
                )
            ),
            on_confirm_dismiss=handle_confirm_dismiss,
            dismiss_thresholds={
                ft.DismissDirection.END_TO_START: 0.2,
                ft.DismissDirection.START_TO_END: 0.2,
            },
        )
        return dismiss

    dis_column = ft.Column(
        expand=True,
        controls=[ build_dismiss() ],
    )
    dis_count = ft.Container(
        ft.Text(f"{counter+1} / {len(dis_src)}", color='WHITE', size=10),
        border_radius=15,
        bgcolor=ft.colors.BLACK54,
        padding=ft.padding.only(10,3,10,3),
        right=20, top=250
    )
    
    page.add( 
        ft.Stack(
            [ dis_column, dis_count ]
        )
    )

ft.app(main)
