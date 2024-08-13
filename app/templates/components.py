import plotly.graph_objects as go


class ComponentesDash:
    def __init__(self):
        pass

    def imagemDraw(self, path_img):
        fig = go.Figure()
        # Add image
        img_width = 1600
        img_height = 900
        scale_factor = 0.5
        fig.add_layout_image(
            x=0,
            sizex=img_width,
            y=0,
            sizey=img_height,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            source=path_img,
        )
        fig.update_xaxes(showgrid=False, range=(0, img_width))
        fig.update_yaxes(showgrid=False, scaleanchor="x", range=(img_height, 0))
        # Line shape added programatically
        fig.add_shape(
            type="line",
            xref="x",
            yref="y",
            x0=650,
            x1=1080,
            y0=380,
            y1=180,
            line_color="cyan",
        )
        # Set dragmode and newshape properties; add modebar buttons
        fig.update_layout(
            dragmode="drawrect",
            newshape=dict(line_color="cyan"),
            title_text="Drag to add annotations - use modebar to change drawing tool",
        )
        fig.show(
            config={
                "modeBarButtonsToAdd": [
                    "drawline",
                    "drawopenpath",
                    "drawclosedpath",
                    "drawcircle",
                    "drawrect",
                    "eraseshape",
                ]
            }
        )
