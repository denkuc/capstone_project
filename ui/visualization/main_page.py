import dash_bootstrap_components as dbc
from dash import html

from ui import NOTEBOOKS_FOLDER_PATH, IMAGE_FOLDER_PATH

# Replace these with your actual image URLs and page links
cards_content = [
    {
        "image_url": IMAGE_FOLDER_PATH + "sectors.png",
        "page_link": "/sectors",
        "description": "Explore Sectors",
        "page_type": "Dashboard",
    },
    {
        "image_url": IMAGE_FOLDER_PATH + "stars.png",
        "page_link": "/stars",
        "description": "Explore Stars",
        "page_type": "Dashboard",
    },
    {
        "image_url": IMAGE_FOLDER_PATH + "data_extraction.png",
        "page_link": NOTEBOOKS_FOLDER_PATH + "1_data_extraction_module.ipynb",
        "description": "Data Extraction Module",
        "page_type": "Jupyter Notebook",
    },
    {
        "image_url": IMAGE_FOLDER_PATH + "transformation.jpg",
        "page_link": NOTEBOOKS_FOLDER_PATH + "2_transformation_module.ipynb",
        "description": "Transformation Module",
        "page_type": "Jupyter Notebook",
    },
    {
        "image_url": IMAGE_FOLDER_PATH + "windowing.jpg",
        "page_link": NOTEBOOKS_FOLDER_PATH + "3_windowing_module.ipynb",
        "description": "Windowing Module",
        "page_type": "Jupyter Notebook",
    },
    {
        "image_url": IMAGE_FOLDER_PATH + "machine_learning.jpg",
        "page_link": NOTEBOOKS_FOLDER_PATH + "4_machine_learning_module.ipynb",
        "description": "Machine Learning Module",
        "page_type": "Jupyter Notebook",
    }
]

# Create cards for each cell
cards = []
for card_content in cards_content:
    card = dbc.Card(
        [
            html.Div(
                dbc.CardImg(src=card_content['image_url'], top=True, style={'object-fit': 'cover', 'object-position': 'center'}),
                style={'height': '342px', 'overflow': 'hidden'}
            ),
            dbc.CardBody(
                [
                    html.H5(card_content['description'], className="card-title"),
                    html.P(card_content['page_type'], className="card-text"),
                ]
            ),
        ]
    )
    # Wrap the Card component in a html.A component to make it clickable
    card_link = html.A(card, href=card_content['page_link'], target="_blank")
    cards.append(card_link)

# Create the grid layout
grid = dbc.Row(
    [dbc.Col(cards[i], width=4) for i in range(6)],
    className="g-4"
)

main_page_dashboard = html.Div([grid])
