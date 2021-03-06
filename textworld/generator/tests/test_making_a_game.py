# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.


import numpy as np

import textworld
from textworld.utils import make_temp_directory
from textworld.generator import World
from textworld.generator import make_quest
from textworld.generator import compile_game


def test_making_a_game_without_a_quest(play_the_game=False):
    rng_map = np.random.RandomState(1234)
    map_ = textworld.generator.make_small_map(1, rng_map)
    world = World.from_map(map_)
    world.set_player_room()  # First room generated (i.e. the only one).

    rng_objects = np.random.RandomState(1234)
    nb_objects = 10
    world.populate(nb_objects, rng=rng_objects)

    quests = []

    # Define the grammar we'll use.
    rng_grammar = np.random.RandomState(1234)
    grammar_flags = {
        "theme": "house",
        "include_adj": False,
        "only_last_action": True,
        "blend_instructions": True,
        "blend_descriptions": True,
        "refer_by_name_only": True,
        "instruction_extension": [],
    }
    grammar = textworld.generator.make_grammar(flags=grammar_flags, rng=rng_grammar)

    # Generate the world representation.
    game = textworld.generator.make_game_with(world, quests, grammar)

    with make_temp_directory(prefix="test_render_wrapper") as tmpdir:
        game_name = "test_making_a_game_without_a_quest"
        game_file = compile_game(game, game_name, games_folder=tmpdir)

        if play_the_game:
            textworld.play(game_file)


def test_making_a_game(play_the_game=False):
    rng_map = np.random.RandomState(1234)
    map_ = textworld.generator.make_small_map(1, rng_map)
    world = World.from_map(map_)
    world.set_player_room()  # First room generated (i.e. the only one).

    rng_objects = np.random.RandomState(123)
    nb_objects = 10
    world.populate(nb_objects, rng=rng_objects)

    rng_quest = np.random.RandomState(124)
    quest = make_quest(world, quest_length=5, rng=rng_quest)

    # Define the grammar we'll use.
    rng_grammar = np.random.RandomState(1234)
    grammar_flags = {
        "theme": "house",
        "include_adj": False,
        "only_last_action": True,
        "blend_instructions": True,
        "blend_descriptions": True,
        "refer_by_name_only": True,
        "instruction_extension": [],
    }
    grammar = textworld.generator.make_grammar(flags=grammar_flags, rng=rng_grammar)

    # Generate the world representation.
    game = textworld.generator.make_game_with(world, [quest], grammar)

    with make_temp_directory(prefix="test_render_wrapper") as tmpdir:
        game_name = "test_making_a_game"
        game_file = compile_game(game, game_name, games_folder=tmpdir)

        if play_the_game:
            textworld.play(game_file)


if __name__ == "__main__":
    # test_making_a_game(play_the_game=True)
    test_making_a_game_without_a_quest(play_the_game=True)
