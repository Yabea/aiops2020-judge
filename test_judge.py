'''
Test suite for judge.py
'''
import json
import os

import pytest

import judge


@pytest.mark.parametrize(('answer_path', 'result_path', 'expectation'), [
    (os.path.join('answer', 'answer-0411.json'), 'sample_result.csv', 120),
    ('nonexistent_answer.json', 'nonexisstent_result.json', 0),
])
def test_judge(answer_path, result_path, expectation):
    '''Test judge.judge'''
    ret = judge.judge(answer_path, result_path)
    assert ret['data'] == expectation, ret['message']


def test_function(capsys):
    '''
    Test judge.main

    Sample data is supposed to be created with insufficient arguments.
    Judging the created sample data is supposed to get a grade of 120.
    '''
    cmd = 'judge.py'
    iters = 2  # Verify idempotence

    for _ in range(iters):
        # Create sample data
        answer_path, result_path, action = judge.main([cmd, ])
        assert action == 'demo'
        _ = capsys.readouterr()
        # Judge with created data
        _, _, action = judge.main([cmd, answer_path, result_path])
        assert action == 'judge'
        captured = capsys.readouterr()
        ret = json.loads(captured.out)
        assert ret['data'] == 120, ret['message']

    result_path = 'result.json'
    judge._demo(answer_path, result_path)  # pylint: disable=protected-access
    _ = capsys.readouterr()
    # Judge with created data
    _, _, action = judge.main([cmd, answer_path, result_path])
    assert action == 'judge'
    captured = capsys.readouterr()
    ret = json.loads(captured.out)
    assert ret['data'] == 120, ret['message']