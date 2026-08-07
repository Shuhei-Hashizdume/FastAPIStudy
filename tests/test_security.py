from security import hash_password, verify_password


def test_hash_password_returns_different_string():
    input_password = "testPW"

    hashed_password = hash_password(input_password)

    assert input_password != hashed_password
    assert isinstance(hashed_password, str)


def test_verify_password_returns_true_for_correct_password():
    input_password = "testPW"

    hashed_password = hash_password(input_password)

    result = verify_password(input_password, hashed_password)

    assert result is True


def test_verify_password_returns_false_for_wrong_password():
    correct_password = "correct-password"

    hashed_password = hash_password(correct_password)

    wrong_password = "wrong-password"

    result = verify_password(wrong_password, hashed_password)

    assert result is False


def test_hash_password_uses_different_salt_each_time():
    same_password = "same_password"

    hashed_password1 = hash_password(same_password)
    hashed_password2 = hash_password(same_password)

    assert hashed_password1 != hashed_password2
