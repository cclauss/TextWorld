# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.


import textworld

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from textworld import g_rng
from textworld.utils import make_temp_directory
from textworld.generator import compile_game
from textworld.envs.wrappers import HtmlViewer


def test_html_viewer():
    # Integration test for visualization service
    # requires geckodriver to be in PATH for selenium to work.
    num_nodes = 3
    num_items = 10
    g_rng.set_seed(1234)
    grammar_flags = {"theme": "house", "include_adj": True}
    game = textworld.generator.make_game(world_size=num_nodes, nb_objects=num_items, quest_length=3, grammar_flags=grammar_flags)

    game_name = "test_html_viewer_wrapper"
    with make_temp_directory(prefix=game_name) as tmpdir:
        game_file = compile_game(game, game_name, games_folder=tmpdir)

        env = textworld.start(game_file)
        env = HtmlViewer(env, open_automatically=False, port=8080)
        env.reset()  # Cause rendering to occur.

    options = Options()
    options.add_argument('headless')
    options.add_argument('ignore-certificate-errors')
    options.add_argument("test-type")
    options.add_argument("no-sandbox")
    options.add_argument("disable-gpu")
    # options.binary_location = "/bin/chromium"

    driver = webdriver.Chrome(chrome_options=options)
    driver.get("http://127.0.0.1:8080")
    nodes = driver.find_elements_by_class_name("node")
    assert len(nodes) == num_nodes
    items = driver.find_elements_by_class_name("item")

    # add one for P
    assert len(items) == num_items + 1

    env.close()
    driver.close()
