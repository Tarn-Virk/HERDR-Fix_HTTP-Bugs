"""Supervisor checks: hits the LIVE server and reports what actually works.
Run with:  python test_api.py
Every check creates its own records, so it can be run again and again."""
import os
import time

import requests

BASE = os.environ.get("API_URL", "http://127.0.0.1:8000")
RUN = str(int(time.time() * 1000))  # makes every email unique per run
results = []


def check(endpoint, name, passed, detail=""):
    results.append((endpoint, name, passed, detail))


def email(tag):
    return f"{tag}.{RUN}@test.dev"


def add(name, tag):
    return requests.post(f"{BASE}/contacts", json={"name": name, "email": email(tag)})


def all_contacts():
    return requests.get(f"{BASE}/contacts").json()


def ids():
    return [c["id"] for c in all_contacts()]


# ---------- GET ----------
r = requests.get(f"{BASE}/contacts")
check("GET", "lists contacts", r.status_code == 200 and isinstance(r.json(), list),
      f"status {r.status_code}")

add("Zed Searchable", "zed")
r = requests.get(f"{BASE}/contacts", params={"search": "zed searchable"})
names = [c["name"] for c in r.json()] if r.status_code == 200 else []
check("GET", "?search= filters by name or email (case-insensitive)",
      r.status_code == 200 and len(names) >= 1 and all("zed" in n.lower() for n in names),
      f"got {len(names)} results: {names[:4]}")

# ---------- POST ----------
r = add("Post Tester", "post")
created = r.json() if r.status_code == 201 else {}
check("POST", "creates a contact (201) that shows up in GET",
      r.status_code == 201 and created.get("id") in ids(), f"status {r.status_code}")

r = add("Post Tester Again", "post")
check("POST", "rejects a duplicate email with 409", r.status_code == 409,
      f"expected 409, got {r.status_code}")

r = requests.post(f"{BASE}/contacts", json={"name": "   ", "email": email("blank")})
check("POST", "rejects a blank name with 400", r.status_code == 400,
      f"expected 400, got {r.status_code}")

# ---------- PUT ----------
c = add("Before Edit", "put").json()
requests.put(f"{BASE}/contacts/{c['id']}", json={"name": "After Edit", "email": c["email"]})
stored = next((x for x in all_contacts() if x["id"] == c["id"]), {})
check("PUT", "update is saved (GET shows the new name)", stored.get("name") == "After Edit",
      f"GET still shows name={stored.get('name')!r}")

r = requests.put(f"{BASE}/contacts/999999", json={"name": "Ghost", "email": email("ghost")})
check("PUT", "unknown id returns 404", r.status_code == 404, f"got {r.status_code}")

# ---------- DELETE ----------
a = add("Delete A", "del-a").json()
b = add("Delete B", "del-b").json()
keep = add("Delete Keep", "del-keep").json()
requests.delete(f"{BASE}/contacts/{a['id']}")
requests.delete(f"{BASE}/contacts/{b['id']}")
current = ids()
right = a["id"] not in current and b["id"] not in current and keep["id"] in current
check("DELETE", "removes exactly the requested contact, nothing else", right,
      f"A gone={a['id'] not in current}, B gone={b['id'] not in current}, "
      f"Keep survived={keep['id'] in current}")

r = requests.delete(f"{BASE}/contacts/999999")
check("DELETE", "unknown id returns 404", r.status_code == 404, f"got {r.status_code}")

# ---------- REPORT ----------
print("\n=== SUPERVISOR REPORT ===")
for endpoint in ["GET", "POST", "PUT", "DELETE"]:
    print(f"\n{endpoint}")
    for ep, name, passed, detail in results:
        if ep == endpoint:
            mark = "PASS" if passed else "FAIL"
            print(f"  [{mark}] {name}" + ("" if passed else f"  ->  {detail}"))

passed = sum(1 for r in results if r[2])
print(f"\n{passed}/{len(results)} checks passed")
raise SystemExit(0 if passed == len(results) else 1)
