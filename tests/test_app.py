"""Test app import."""


def test_app_import():
    """Test that the app module can be imported."""
    import app
    assert app is not None


def test_streamlit_import():
    """Test that streamlit can be imported."""
    import streamlit as st
    assert st is not None
