class Vacancy:
    def __init__(self, title: str, url: str, salary: dict, description: str):
        self.title = title
        self.url = url
        self.description = description or ''
        self.salary = salary or {}
        self.currency = self.salary.get("currency", "RUR") if self.salary else "RUR"

    @property
    def salary_from(self) -> int:
        try:
            value = self.salary.get("from")
            return int(value) if value is not None else 0
        except (TypeError, ValueError):
            return 0

    @property
    def salary_to(self) -> int:
        try:
            value = self.salary.get("to")
            return int(value) if value is not None else 0
        except (TypeError, ValueError):
            return 0

    def __lt__(self, other) -> bool:
        return self.salary_from < other.salary_from

    def __repr__(self):
        return f"Vacancy({self.title}, {self.salary_from}-{self.salary_to} {self.currency})"

    @classmethod
    def cast_to_object_list(cls, data: list) -> list:
        return [
            cls(
                title=item.get("name"),
                url=item.get("alternate_url"),
                salary=item.get("salary") or {},
                description=item.get("snippet", {}).get("requirement", ""),
            )
            for item in data
            if item.get("name") and item.get("alternate_url")
        ]
