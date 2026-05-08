#!/usr/bin/python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import json

# This returns a dict mapping product names to sets of component names.
# It takes the file name for a components-normalized.json file from the
# Bugzilla job on TreeHerder.
def load_components_json(file_name):
    with open(file_name, "r") as f:
        data = json.load(f)

    products = {}
    for c in data["components"].values():
        assert isinstance(c, list)
        assert len(c) == 2
        product = c[0]
        component = c[1]
        products.setdefault(product, set([])).add(component)

    return products


def bmo_rest(products):
    print("https://bugzilla.mozilla.org/rest/product?" +
          "&".join([f"names={p}" for p in sorted(products.keys())]))

def load_actual_products_json(actual_products_file_name):
    with open(actual_products_file_name, "r") as f:
        data = json.load(f)

    actual_products = {}

    for p in data["products"]:
        component_names = set([])
        for c in p["components"]:
            component_names.add(c["name"])

        actual_products[p["name"]] = component_names

    return actual_products

def print_bad_bug_components(type_name, bad_bug_components):
    if len(bad_bug_components) == 0:
        return

    print(f"BUG_COMPONENT with an invalid {type_name}:")
    for bc in bad_bug_components:
        print(f'  ("{bc[0]}", "{bc[1]}")')
    print("")

def validate_products(products, actual_products_file_name):
    actual_products = load_actual_products_json(actual_products_file_name)

    missing_products = []
    missing_components = []

    for p, components in products.items():
        if p not in actual_products:
            for c in components:
                missing_products.append([p, c])
            continue

        actual_components = actual_products[p]
        for c in components:
            if c in actual_components:
                continue
            missing_components.append([p, c])

    print_bad_bug_components("product", missing_products)
    print_bad_bug_components("component", missing_components)

    if len(missing_products) == 0 and len(missing_components) == 0:
        print("No invalid BUG_COMPONENTs found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate BUG_COMPONENT components against Bugzilla.")

    parser.add_argument("file_name",
                        help="components-normalized.json file from the Bugzilla job on TreeHerder")

    parser.add_argument("--bmo", dest="bmo_rest", action="store_true",
                        default=False,
                        help="If set, print out a Bugzilla REST API URL for all of the products.")

    parser.add_argument("--products", type=str,
                        help="Name of the products JSON file from Bugzilla to validate against.")

    args = parser.parse_args()

    products = load_components_json(args.file_name)

    if args.bmo_rest:
        bmo_rest(products)
    else:
        validate_products(products, args.products)
