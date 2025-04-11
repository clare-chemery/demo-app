"""This script performs data tranformations and cleaning on the raw data to create a tailored dataset for the demo app."""

import pandas as pd
import numpy as np
import logging
from pathlib import Path


def main():
    # ------ Load Data ------
    # Only keep necessary columns
    logging.info("Loading data.")

    inventory_parts = pd.read_csv(
        Path(__file__).parent / "raw_data/rebrickable/inventory_parts_reduced.csv"
    )[["part_num", "color_id", "quantity", "img_url"]]

    parts = pd.read_csv(Path(__file__).parent / "raw_data/rebrickable/parts.csv")[
        ["part_num", "name", "part_cat_id"]
    ]
    parts.rename(columns={"name": "part_name"}, inplace=True)

    part_categories = pd.read_csv(
        Path(__file__).parent / "raw_data/rebrickable/part_categories.csv"
    )
    part_categories.rename(columns={"name": "part_cat_name"}, inplace=True)

    colors = pd.read_csv(Path(__file__).parent / "raw_data/rebrickable/colors.csv")[
        ["id", "name", "rgb"]
    ]
    colors.rename(columns={"name": "color_name"}, inplace=True)

    # ------ Explode inventory_parts to get a row per piece ------
    logging.info("Exploding inventory_parts.")
    inventory_parts["quantity"] = inventory_parts.quantity.apply(
        lambda q: np.repeat(1, q)
    )
    inventory_parts = inventory_parts.explode("quantity").drop("quantity", axis=1)

    # ------ Merge parts with inventory_parts to get the part category and color ------
    logging.info("Merging inventory_parts with parts.")
    lego_pile = inventory_parts.merge(parts, on="part_num", how="left")

    logging.info("Adding part categories.")
    lego_pile = lego_pile.merge(
        part_categories, left_on="part_cat_id", right_on="id", how="left"
    ).drop("id", axis=1)

    logging.info("Adding colors.")
    lego_pile = lego_pile.merge(
        colors, left_on="color_id", right_on="id", how="left"
    ).drop("id", axis=1)

    # ------ Take only part of the data (too big for Git) ------
    # Remove unnecessary columns
    lego_pile = lego_pile[
        ["img_url", "part_name", "part_cat_name", "color_name", "rgb"]
    ]
    # Removing some non-Lego parts (Other and Stickers)
    lego_pile = lego_pile[~(lego_pile.part_cat_name == "Other")]
    lego_pile = lego_pile[~(lego_pile.part_cat_name == "Stickers")]
    # Taking a further random sample to reduce size
    lego_pile = lego_pile.sample(800000)

    # ------ Save to csv ------
    logging.info("Saving to csv.")
    lego_pile.to_csv(
        Path(__file__).parent.parent / "app/data/lego_pile.csv", index=False
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
