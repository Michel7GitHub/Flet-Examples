import flet as ft
import flet_map as map
import json

class MyMap(ft.Container):
    def __init__(self, url_template, initial_center, zoom, handle_tap=None, zoom_button=False):
        super().__init__()

        self.url_template = url_template
        self.initial_center = initial_center
        self.zoom = zoom
        self.handle_tap = handle_tap

        self.expand = True

        self.circles = []
        self.polylines = []
        self.markers = []

        self.tile_layer = map.TileLayer(url_template = self.url_template)
        self.circle_layer = map.CircleLayer(circles = self.circles)
        self.polyline_layer = map.PolylineLayer(polylines = self.polylines)
        self.marker_layer = map.MarkerLayer(markers = self.markers)

        self.marker_pointer = None
        self.marker_spot = None
        self.selected_marker = None

        (lat, lon) = self.initial_center

        self.mymap = map.Map(
            expand = True,
            initial_center = map.MapLatitudeLongitude(lat, lon),
            initial_zoom = self.zoom,
            interaction_configuration=map.MapInteractionConfiguration(
                flags=map.MapInteractiveFlag.ALL & ~map.MapInteractiveFlag.ROTATE
            ),
            on_tap = self.handle_tap,
            layers=[ 
                self.tile_layer,
                self.circle_layer,
                self.polyline_layer,
                self.marker_layer
            ]
        )


        #   ZOOM-out & ZOOM-in buttons
        # ========================================================
        self.zoom_button = ft.Container(
            content = ft.Column(
                [
                    ft.IconButton(
                        icon=ft.Icons.ADD_OUTLINED,
                        style=ft.ButtonStyle(
                            bgcolor={"": ft.Colors.WHITE},
                            padding={ft.ControlState.DEFAULT: 0},
                            color={ ft.ControlState.DEFAULT: ft.Colors.BLACK45 },
                            side={ ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.GREY_200) },
                            shape={ ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=7) },
                        ),
                        on_click=lambda _: self.mymap.zoom_in(),
                        height=36, width=36
                    ),

                    ft.IconButton(
                        icon=ft.Icons.HORIZONTAL_RULE_OUTLINED,
                        style=ft.ButtonStyle(
                            bgcolor={"": ft.Colors.WHITE},
                            padding={ft.ControlState.DEFAULT: 0},
                            color={ ft.ControlState.DEFAULT: ft.Colors.BLACK45 },
                            side={ ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.GREY_200) },
                            shape={ ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=7) },
                        ),
                        on_click = lambda _: self.mymap.zoom_out(),
                        height=36, width=36
                    )
                ],
                spacing=0
            ),
            width=40,
            visible=zoom_button
        )


        #   BUILD FINAL Conatiner
        # =======================================================================

        self.top_left = ft.Container(
            ft.Row([ self.zoom_button ]),
            top=10, left=10
        )

        self.content = ft.Stack(
            [
                self.mymap,
                self.top_left
            ]
        )


    #   SET Map Tile
    # ===============================================================================    
    def set_url_template(self, url_template): 
        return map.TileLayer( url_template = url_template )


    #   CENTER ON
    # ====================================================================================
    def center_on(self, lat, lon, zoom=None, curve=ft.AnimationCurve.EASE_OUT_CIRC, duration=1000):
        if zoom != None:
            self.zoom = zoom
        self.mymap.center_on(
            map.MapLatitudeLongitude(lat, lon), 
            zoom=self.zoom,
            animation_curve=curve,
            animation_duration=duration
        )
        self.mymap.update()


    #   MOVE TO
    # ====================================================================================
    def move_to(self, lat, lon, zoom=None, curve=ft.AnimationCurve.EASE_OUT_CIRC, duration=1000):
        if zoom != None:
            self.zoom = zoom
        self.mymap.move_to(
            map.MapLatitudeLongitude(lat, lon), 
            zoom=self.zoom,
            animation_curve=curve,
            animation_duration=duration
        )
        self.mymap.update()


    #   ZOOM TO
    # ====================================================================================
    def zoom_to(self, zoom, curve=ft.AnimationCurve.EASE_OUT_CIRC, duration=1000):
        self.mymap.zoom_to(
            zoom=zoom,
            animation_curve=curve,
            animation_duration=duration
        )
        self.mymap.update() 


    #   ADD Marker to map
    # ===============================================================================

    def add_marker(self, lat, lon, 
            icon_name='LOCATION_PIN',  
            icon_size=18,
            icon_color='white',
            shape=ft.BoxShape.CIRCLE,
            width=28,
            height=28, 
            bgcolor='white', 
            border_width=1, 
            border_color='white',
            alignment=ft.alignment.top_center ):

        marker = map.Marker(	
            ft.Container(
                ft.Icon( icon_name, size=icon_size, color=icon_color ),
                shape=shape,
                width=width, height=height,
                bgcolor=bgcolor,
                border=ft.border.all(border_width, border_color),
                on_click=self.on_click_marker
            ),
            width=width, height=width,
            alignment=alignment,
            coordinates = map.MapLatitudeLongitude(lat, lon)
        )
        self.markers.append(marker)
        return marker
    

    #   ADD Marker-Pointer to map
    # ===============================================================================

    def add_marker_pointer(self, lat, lon, 
            icon_name='GPS_FIXED', 
            icon_size=18,
            icon_color='black', 
            shape=ft.BoxShape.CIRCLE, 
            bgcolor='transparent',
            width=28, 
            height=28 ):

        marker = map.Marker(	
            ft.Container(
                ft.Icon( icon_name, size=icon_size, color=icon_color ),
                width=width, height=height,
                shape=shape,
                bgcolor=bgcolor,
                on_click=self.on_click_marker
            ),
            width=width, height=width,
            alignment=ft.alignment.center,
            coordinates = map.MapLatitudeLongitude(lat, lon)
        )
        self.marker_pointer = marker
        self.markers.append(marker)
        return marker
    

    #   ADD Marker-Spot (Chart Spot) to map
    # ===============================================================================

    def add_marker_spot(self, lat, lon, 
            icon_name='CIRCLE_ROUNDED',  
            icon_size=12,
            icon_color=ft.Colors.LIME_ACCENT_700,
            width=12, 
            height=12,
            shape=ft.BoxShape.CIRCLE ):

        if self.marker_spot != None:
            self.remove_marker(self.marker_spot)
            
        marker = map.Marker(	
            ft.Container(
                ft.Icon( icon_name, size=icon_size, color=icon_color ),
                width=width, height=height,
                shape=shape
            ),
            width=width, height=width,
            alignment=ft.alignment.center,
            coordinates = map.MapLatitudeLongitude(lat, lon)
        )
        self.marker_spot = marker
        self.markers.append(marker)
        return marker
    

    #   Remove Marker from map
    # ===============================================================================    
    def remove_marker(self, marker):
        self.markers.remove(marker)


    #   User click on Marker
    # =============================================================================== 
    def on_click_marker(self, e):
        e_marker = e.control.parent
 
        if self.marker_pointer == e_marker:
            self.remove_marker(self.marker_pointer)
            self.marker_pointer = None
            self.marker_layer.update()
            return
        
        if self.marker_pointer != None:
            self.remove_marker(self.marker_pointer)
            self.marker_pointer = None
        
        if self.selected_marker == None:
            self.select_marker(e_marker)
            self.selected_marker = e_marker
        elif self.selected_marker == e_marker:
            self.unselect_marker(self.selected_marker)
            self.selected_marker = None
        else:
            self.unselect_marker(self.selected_marker)
            self.select_marker(e_marker)
            self.selected_marker = e_marker
        self.marker_layer.update()


    #   Select Marker... change its appearance (Colors and ...)
    # ===============================================================================    
    def select_marker(self, marker):
        # Exit if Marker already selected 
        if marker.content.bgcolor == 'white':
            return
        marker.content.content.color = marker.content.bgcolor
        marker.content.bgcolor = 'white'
        marker.content.border = ft.border.all(1, 'black45')
        self.selected_marker = marker
        self.marker_layer.update()


    #   Unselect Marker appearance (Colors and ...)
    # ===============================================================================    
    def unselect_marker(self, marker):
        # Exit if Marker already unselected 
        if marker.content.content.color == 'white':
            return
        marker.content.bgcolor = marker.content.content.color
        marker.content.content.color = 'white'
        marker.content.border = ft.border.all(1.5, 'white')
        self.selected_marker = None
        self.marker_layer.update()


    #   ADD Polyline to map
    # ===============================================================================    
    def add_polyline(self, coordinates, color='red', width=3):
        # Create all points for polyline
        point_list = []
        for (lat, lon, elev) in json.loads(coordinates):
            point_list.append(map.MapLatitudeLongitude(lat, lon))

        polyline = map.PolylineMarker(
            border_stroke_width=width,
            border_color=color,
            gradient_colors=[ft.Colors.BLACK, ft.Colors.BLACK],
            color=ft.Colors.with_opacity(0.6, ft.Colors.GREEN),
            coordinates = point_list
        ) 
        self.polylines.append(polyline)
        return polyline
    

    #   Remove Polyline from map
    # ===============================================================================    
    def remove_polyline(self, polyline):
        self.polylines.remove(polyline)
