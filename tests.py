import pytest
from main import BooksCollector


class TestBooksCollector:
    @pytest.fixture
    def collector(self):
        return BooksCollector()

    @pytest.mark.parametrize(
        "name, expected",
        [
            ("Нормальная книга", True),
            ("", False),
            (
                "Очень длинное название книги, которое явно превышает лимит в 40 символов",
                False,
            ),
        ],
    )
    def test_add_new_book_validation(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected

    def test_new_book_has_no_genre(self, collector):
        collector.add_new_book("Книга без жанра")
        assert collector.get_book_genre("Книга без жанра") == ""

    def test_get_book_genre_returns_correct_genre(self, collector):
        collector.books_genre = {"Тестовая книга": "Фантастика"}
        assert collector.get_book_genre("Тестовая книга") == "Фантастика"

    def test_age_rated_books_not_in_children_list(self, collector):
        collector.add_new_book("Детская книга")
        collector.add_new_book("Страшная книга")
        collector.add_new_book("Детективная книга")

        collector.set_book_genre("Детская книга", "Мультфильмы")
        collector.set_book_genre("Страшная книга", "Ужасы")
        collector.set_book_genre("Детективная книга", "Детективы")

        children_books = collector.get_books_for_children()

        assert "Детская книга" in children_books
        assert "Страшная книга" not in children_books
        assert "Детективная книга" not in children_books

    def test_set_book_genre_valid_genre(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Фантастика")
        assert collector.get_book_genre("Книга") == "Фантастика"

    def test_set_book_genre_invalid_genre(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Несуществующий жанр")
        assert collector.get_book_genre("Книга") == ""

    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book("Фантастика 1")
        collector.add_new_book("Фантастика 2")
        collector.set_book_genre("Фантастика 1", "Фантастика")
        collector.set_book_genre("Фантастика 2", "Фантастика")
        books = collector.get_books_with_specific_genre("Фантастика")
        assert len(books) == 2
        assert "Фантастика 1" in books
        assert "Фантастика 2" in books

    def test_add_to_favorites(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        assert "Книга" in collector.get_list_of_favorites_books()

    def test_remove_from_favorites(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")
        assert "Книга" not in collector.get_list_of_favorites_books()

    def test_add_non_existent_book_to_favorites(self, collector):
        collector.add_book_in_favorites("Несуществующая книга")
        assert "Несуществующая книга" not in collector.get_list_of_favorites_books()
