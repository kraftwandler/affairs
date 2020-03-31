from big_ol_pile_of_manim_imports import *

class Grid(VMobject):
    CONFIG = {
        "height": 6.0,
        "width": 6.0,
    }

    def __init__(self, rows, columns, **kwargs):
        digest_config(self, kwargs, locals())
        VMobject.__init__(self, **kwargs)

    def generate_points(self):
        x_step = self.width / self.columns
        y_step = self.height / self.rows

        for x in np.arange(0, self.width + x_step, x_step):
            self.add(Line(
                [x - self.width / 2., -self.height / 2., 0],
                [x - self.width / 2., self.height / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width / 2., y - self.height / 2., 0],
                [self.width / 2., y - self.height / 2., 0]
            ))


class ScreenGrid(VGroup):
    CONFIG = {
        "rows":8,
        "columns":14,
        "height": FRAME_Y_RADIUS*2,
        "width": 14,
        "grid_stroke":0.5,
        "grid_color":WHITE,
        "axis_color":RED,
        "axis_stroke":2,
        "show_points":False,
        "point_radius":0,
        "labels_scale":0.5,
        "labels_buff":0,
        "number_decimals":2
    }

    def __init__(self,**kwargs):
        VGroup.__init__(self,**kwargs)
        rows=self.rows
        columns=self.columns
        grilla=Grid(width=self.width,height=self.height,rows=rows,columns=columns).set_stroke(self.grid_color,self.grid_stroke)

        vector_ii=ORIGIN+np.array((-self.width/2,-self.height/2,0))
        vector_id=ORIGIN+np.array((self.width/2,-self.height/2,0))
        vector_si=ORIGIN+np.array((-self.width/2,self.height/2,0))
        vector_sd=ORIGIN+np.array((self.width/2,self.height/2,0))

        ejes_x=Line(LEFT*self.width/2,RIGHT*self.width/2)
        ejes_y=Line(DOWN*self.height/2,UP*self.height/2)

        ejes=VGroup(ejes_x,ejes_y).set_stroke(self.axis_color,self.axis_stroke)

        divisiones_x=self.width/columns
        divisiones_y=self.height/rows

        direcciones_buff_x=[UP,DOWN]
        direcciones_buff_y=[RIGHT,LEFT]
        dd_buff=[direcciones_buff_x,direcciones_buff_y]
        vectores_inicio_x=[vector_ii,vector_si]
        vectores_inicio_y=[vector_si,vector_sd]
        vectores_inicio=[vectores_inicio_x,vectores_inicio_y]
        tam_buff=[0,0]
        divisiones=[divisiones_x,divisiones_y]
        orientaciones=[RIGHT,DOWN]
        puntos=VGroup()
        leyendas=VGroup()


        for tipo,division,orientacion,coordenada,vi_c,d_buff in zip([columns,rows],divisiones,orientaciones,[0,1],vectores_inicio,dd_buff):
            for i in range(1,tipo):
                for v_i,direcciones_buff in zip(vi_c,d_buff):
                    ubicacion=v_i+orientacion*division*i
                    punto=Dot(ubicacion,radius=self.point_radius)
                    coord=round(punto.get_center()[coordenada],self.number_decimals)
                    leyenda=TextMobject("%s"%coord).scale(self.labels_scale)
                    leyenda.next_to(punto,direcciones_buff,buff=self.labels_buff)
                    puntos.add(punto)
                    leyendas.add(leyenda)

        self.add(grilla,ejes,leyendas)
        if self.show_points==True:
            self.add(puntos)

class BoxPushi(MovingCameraScene):
    def construct(self):
        grid=ScreenGrid()
        #self.add(grid)
        line = Line([-7,-1/2,0],[7,-1/2,0])
        rect = Rectangle(height=1,width=1)
        rect.set_fill(PINK, opacity=0.5)
        self.play(ShowCreation(line),ShowCreation(rect))
        self.wait()
        Text1=TextMobject("?");
        Text1.move_to([-3/2,1/2,0])
        
        #arrowtransform
        arr1 = Arrow([-2,0,0],[-1/2,0,0])
        arr1.next_to(rect,0.1*LEFT)
        arr1.set_color(BLUE)
        self.play(Write(Text1),GrowArrow(arr1))
        self.wait(1)
        arr2 = Arrow([-3,0,0],[-1/2,0,0])
        arr2.set_color(BLUE)
        arr2.next_to(rect,0.1*LEFT)
        self.play(ReplacementTransform(arr1,arr2),run_time=2)
        self.wait(1)
        Question1=TextMobject("Why doesn't the box move?")
        Question1.move_to([0,2,0])
        self.play(Write(Question1))
        self.wait(2)
        
        #ZoomIn
        Text2=TexMobject("F_1");
        Text2.move_to([-3/4,1/4,0])
        Text2.scale(0.5)
        arr3 = Arrow([-3/2,0,0],[-1/2,0,0])
        arr3.next_to(rect,0.1*LEFT)
        arr3.set_color(BLUE)
        self.play(FadeOut(Question1),FadeOut(Text1))
        self.wait()
        self.camera_frame.save_state()
        self.play(
            ReplacementTransform(arr2,arr3),
            Write(Text2),
            # Set the size with the width of a object
            self.camera_frame.set_width,rect.get_width()*7.2,
            # Move the camera to the object
            self.camera_frame.move_to,[-1,0,0]
        )
        self.wait(3)
        
        #Newton
        momentum1=TexMobject(
            "\\frac{dp}{dt} = F"
        )
        momentum1.move_to(5/2*LEFT)
        momentum1.scale(0.8)
        self.play(Write(momentum1))
        self.wait(1)
        momentum2=TexMobject(
            "\\frac{d(mv)}{dt} = F"
        )
        momentum2.move_to(5/2*LEFT)
        momentum2.scale(0.8)
        self.play(ReplacementTransform(momentum1,momentum2))
        self.wait(1)
        momentum3=TexMobject(
            "m\\frac{dv}{dt} = F"
        )
        momentum3.move_to(5/2*LEFT)
        momentum3.scale(0.8)
        self.play(ReplacementTransform(momentum2,momentum3))
        self.wait(1)
        momentum4=TexMobject(
            "ma = F"
        )
        momentum4.move_to(5/2*LEFT)
        momentum4.scale(0.8)
        self.play(ReplacementTransform(momentum3,momentum4))
        self.wait(1)
        momentum5=TexMobject(
            "F = ma"
        )
        momentum5.move_to(5/2*LEFT)
        momentum5.scale(0.8)
        self.play(ReplacementTransform(momentum4,momentum5))
        framebox1 = SurroundingRectangle(momentum5, buff = .1)
        self.play(
            ShowCreation(framebox1),
            )
        self.wait(1)
        momentum5.shift(UP)
        framebox1.shift(UP)
        self.play(Write(momentum5),Write(framebox1))
        
        #NumbersIn
        eq1=TexMobject(
            "F = 0"
        )
        eq1.move_to(5/2*LEFT)
        eq1.scale(0.8)
        self.play(Write(eq1))
        self.wait(1)
        eq2=TexMobject(
            "F_1 = 0 ?"
        )
        eq2.move_to(5/2*LEFT)
        eq2.scale(0.8)
        self.play(ReplacementTransform(eq1,eq2))
        Text3=TextMobject("We know that ${F_1}$ is not 0.")
        Text3.move_to(5/2*LEFT+DOWN)
        Text3.scale(0.5)
        self.play(Write(Text3))

        #PanRight
        self.play(FadeOut(Text3),FadeOut(eq2),FadeOut(framebox1),FadeOut(momentum5))
        self.play(
            # Set the size with the width of a object
            self.camera_frame.set_width,rect.get_width()*7.2,
            # Move the camera to the object
            self.camera_frame.move_to,[3/2,0,0]
        )
        Text4=TextMobject("There has to be an opposing force...")
        Text4.move_to(5/2*RIGHT+UP)
        Text4.scale(0.5)
        self.play(Write(Text4))
        arrn1 = Arrow([3/2,0,0],[1/2,0,0])
        arrn1.next_to(rect,0.1*RIGHT)
        arrn1.set_color(BLUE)
        Text5=TexMobject("F_f");
        Text5.move_to([3/4,1/4,0])
        Text5.scale(0.5)
        self.play(GrowArrow(arrn1),Write(Text5))
        Text6=TextMobject("...exactly as big as ${F_1}$.")
        Text6.move_to(5/2*RIGHT+DOWN)
        Text6.scale(0.5)
        self.play(Write(Text6))

