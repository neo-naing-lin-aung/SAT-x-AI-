from types import SimpleNamespace

from django.test import TestCase

from .views import _extract_response_text


class ExtractResponseTextTests(TestCase):
    def test_returns_response_text_when_available(self):
        response = SimpleNamespace(
            text="  Here is the explanation.  ",
            candidates=[],
        )

        self.assertEqual(_extract_response_text(response), "Here is the explanation.")

    def test_extracts_text_from_later_candidate_when_response_text_is_empty(self):
        response = SimpleNamespace(
            text=None,
            candidates=[
                SimpleNamespace(
                    content=SimpleNamespace(
                        parts=[SimpleNamespace(text=" ", thought=False)]
                    )
                ),
                SimpleNamespace(
                    content=SimpleNamespace(
                        parts=[SimpleNamespace(text="The explanation.", thought=False)]
                    )
                ),
            ],
        )

        self.assertEqual(_extract_response_text(response), "The explanation.")

    def test_ignores_thought_parts(self):
        response = SimpleNamespace(
            text=None,
            candidates=[
                SimpleNamespace(
                    content=SimpleNamespace(
                        parts=[
                            SimpleNamespace(text="Internal thought.", thought=True),
                        ]
                    )
                ),
            ],
        )

        self.assertIsNone(_extract_response_text(response))
