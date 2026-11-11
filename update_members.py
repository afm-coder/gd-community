
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# GD Community Chess.com club
API_URL = "https://api.chess.com/pub/club/gd-community"

OUTPUT_FILE = Path("members.json")


def get_member_count():
    request = urllib.request.Request(
        API_URL,
        headers={
            "User-Agent": "GDCommunityMemberTracker/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))

    count = data.get("members_count")

    if not isinstance(count, int) or count < 0:
        raise ValueError("Chess.com returned an invalid member count.")

    return count


def main():
    count = get_member_count()

    result = {
        "club": "GD Community",
        "members": count,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": "Chess.com PubAPI"
    }

    OUTPUT_FILE.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8"
    )

    print(f"GD Community currently has {count} members.")


if __name__ == "__main__":
    main()

