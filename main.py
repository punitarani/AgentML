"""main.py"""

from uuid import UUID

from agentml import Manager
from config import DATA_DIR


def main() -> None:
    """Main function"""
    session_id = UUID("11111111-1111-1111-1111-111111111111")

    manager = Manager(
        goal="Build a classifier",
        csv=DATA_DIR.joinpath("data.csv"),
        session_id=session_id,
    )

    manager.run()


if __name__ == "__main__":
    main()
