"""Where each field sits on Great Eastern form NBZ-FNOMI-V07-082025 (pages 1-5).

Coordinates are PDF points (x, y), measured from the form's own box drawings
(see boxes.py). A point only needs to land inside the right row of boxes;
the filler snaps to the real cell edges. Checkbox points are box centres.

If Great Eastern issues a new version of the form, this file must be re-checked.
"""
FORM_CODE = "NBZ-FNOMI-V07-082025"

# Proposal No / Policy No header boxes on every page: page -> {field: point}
HEADER = {p: {"proposal_no": (px, y), "policy_no": (421, y)}
          for p, (px, y) in {1: (145, 67), 2: (155, 58), 3: (155, 53), 4: (145, 51), 5: (145, 52)}.items()}

# ---- Page 1: proposer / policyowner
OWNER = {
    "page": 1,
    "name": (170, 95),
    "nric": (170, 112),
    "muslim": {"No": (453, 113), "Yes": (493, 113)},
    "status": {"Married": (76.5, 128), "Single": (124.3, 128), "Divorced": (168, 128), "Widowed": (219.7, 128)},
    "children": {"No": (400.5, 128.4), "Yes": (440.3, 128.4)},
    "children_count": [(538.6, 128.7), (549, 128.7)],
}

RELATIONSHIPS = ["Husband", "Wife", "Son", "Daughter", "Father", "Mother", "Brother", "Sister", "Others"]


def _nominee(page, dx, name_ys, nric_y, share_y, gender_y, nat_y, rel_y, addr_ys, town_y, country_y, rel_x):
    return {
        "page": page,
        "name": [(160 + dx, y) for y in name_ys],
        "nric": (110 + dx, nric_y),
        "passport_expiry": [(375 + dx, nric_y), (418 + dx, nric_y), (460 + dx, nric_y)],  # D M Y
        "share": [(496 + dx, share_y), (529 + dx, share_y)],  # whole, decimal
        "gender": {"Male": (114 + dx, gender_y), "Female": (167 + dx, gender_y)},
        "dob": [(375 + dx, gender_y), (418 + dx, gender_y), (460 + dx, gender_y)],
        "nationality": {"Malaysian": (114 + dx, nat_y), "Others": (167 + dx, nat_y)},
        "nationality_other": (262 + dx, nat_y),
        "relationship": {r: (x + 5.7, rel_y) for r, x in zip(RELATIONSHIPS, rel_x)},
        "relationship_other": (505 + dx, rel_y - 6.5, 561 + dx, rel_y + 6.5),
        "address": [(110 + dx, y) for y in addr_ys],
        "postcode": (110 + dx, town_y),
        "town": (208 + dx, town_y),
        "country": (110 + dx, country_y),
    }


_REL_X1 = [106.8, 157.2, 196.0, 233.2, 284.2, 328.1, 373.0, 419.2, 461.2]
_REL_X2 = [107.5, 157.9, 196.8, 234.0, 285.0, 328.9, 373.8, 419.9, 462.0]
NOMINEES = [
    _nominee(1, 0.0, (584, 598, 612), 631, 648, 650, 669, 687.2, (705, 719, 733), 747, 761, _REL_X1),
    _nominee(2, 0.8, (96, 110, 124), 151.5, 167.4, 178, 203, 225.8, (251, 265, 279), 293, 306.6, _REL_X2),
    _nominee(2, 0.8, (345, 358, 372), 397, 409.4, 420.5, 445, 466.6, (488, 502, 516), 530, 544, _REL_X2),
    _nominee(2, 0.8, (577, 591, 605), 627.3, 642, 650, 672.5, 694.5, (718, 732, 746), 759.4, 773.4, _REL_X2),
]

# ---- Page 3: Part 1 declaration (signature date left blank on purpose)
PART1_SIGN = {
    "page": 3,
    "owner_name": (76.0, 330.0, 163.6, 344.9),
    "witness_name": (228.7, 330.0, 316.3, 345.0),
    "witness_iac": (294.8, 348.6, 373.9, 363.6),
}
WITNESS_P3 = {
    "page": 3,
    "name": [(162, 417), (162, 431)],
    "nric": (162, 459),
    "passport_expiry": [(445, 459), (489, 459), (531, 459)],
    "dob": [(133, 484), (177, 484), (218, 484)],
    "address": [(113, 512), (113, 526), (113, 540)],
    "postcode": (113, 553.7),
    "town": (211, 553.7),
    "country": (113, 567.5),
}
PART2_OPTIONS = {  # page 3 checkboxes
    "Appoint": (40.6, 674.5),
    "Appoint in addition to existing": (40.6, 688),
    "Revoke existing and appoint": (40.6, 701.2),
    "Revoke all existing": (40.6, 714.7),
}


def _trustee(dy):
    y = lambda v: v + dy
    return {
        "page": 4,
        "name": [(159, y(88)), (159, y(102)), (159, y(116))],
        "nric": (159, y(135)),
        "passport_expiry": [(449, y(135)), (492, y(135)), (534, y(135))],
        "gender": {"Male": (107.3, y(152.3)), "Female": (163.7, y(152.3))},
        "dob": [(449, y(152.7)), (492, y(152.7)), (534, y(152.7))],
        "nationality": {"Malaysian": (107.3, y(169.8)), "Others": (163.6, y(169.8))},
        "nationality_other": (260, y(169.8)),
        "country_of_birth": {"Malaysian": (107.3, y(187.1)), "Others": (163.6, y(187.1))},
        "country_of_birth_other": (260, y(187.1)),
        "tel": (78, y(204.6)),
        "tel_country": (268, y(204.4)),
        "tel_type": {"House": (432.7, y(204.4)), "Handphone": (470.9, y(204.4)), "Office": (528.3, y(204.4))},
        "address": [(103, y(221)), (103, y(235)), (103, y(249))],
        "postcode": (103, y(262.8)),
        "town": (204, y(262.8)),
        "country": (103, y(276.6)),
    }


TRUSTEES = [_trustee(0), _trustee(210.5)]

PART2_SIGN = {
    "page": 4,
    "owner_name": (65.0, 754.3, 152.6, 769.2),
    "trustee_names": [(199.0, 754.3, 286.6, 769.2), (330.6, 754.3, 418.3, 769.2)],
    "witness_name": (464.6, 754.3, 552.2, 769.2),
    "witness_iac": (496.3, 772.9, 552.2, 787.9),
}
WITNESS_P5 = {
    "page": 5,
    "name": [(161, 84), (161, 98)],
    "nric": (161, 115.5),
    "passport_expiry": [(450, 115.6), (494, 115.6), (536, 115.6)],
    "dob": [(174, 132.2), (217, 132.2), (259, 132.2)],
    "address": [(117, 149.7), (117, 163.7), (117, 177.7)],
    "postcode": (117, 191),
    "town": (215, 191),
    "country": (117, 205),
}
