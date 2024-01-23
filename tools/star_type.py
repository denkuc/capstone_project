from typing import Optional

import requests as r
from bs4 import BeautifulSoup


def get_text_before_description(soup):
    """ extracts the star type from html content """
    # Find the meta tag with name="description" where our Star type is written
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    if not meta_tag:
        return None

    # Navigate backwards from the meta tag to find the text after "--"
    for sibling in meta_tag.previous_siblings:
        if sibling.text and '--' in sibling.text:
            parts = sibling.text.split('--')
            if len(parts) > 1:
                # Return the text after "--", stripped of any leading/trailing whitespace
                return parts[-1].strip()

    return None


def get_star_type(star_tic: str) -> Optional[str]:
    simbad_url_template = 'https://simbad.u-strasbg.fr/simbad/sim-basic?Ident=TIC{}&submit=SIMBAD+search'
    html_content = r.get(simbad_url_template.format(star_tic)).content
    soup = BeautifulSoup(html_content)

    star_type = get_text_before_description(soup)

    return star_type
