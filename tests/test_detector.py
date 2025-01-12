# -*- coding: utf-8 -*-
# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)
"""UpNext detector tests"""

from __future__ import absolute_import, division, unicode_literals
from PIL import Image
import detector


SKIP_TEST_ALL = False
SKIP_TEST_REP_HASH = False
SKIP_TEST_HASH_COMPARE = False


# Test comparisons sourced from:
# https://github.com/valbok/img.chk/blob/master/tests/hash/extractor.py
# Test images sourced from:
# https://github.com/valbok/img.chk/blob/master/tests/images
IMAGE_PAIRS = (
    ('1_500.jpg', '1_500_bl.jpg', True),
    ('1_500.jpg', '1_500_bl2.jpg', True),
    ('1_500.jpg', '1_500_c1.jpg', True),
    ('1_500.jpg', '1_500_cr.jpg', True),
    ('1_500.jpg', '1_500_f.jpg', True),
    ('1_500.jpg', '1_500_left.jpg', True),
    ('1_500.jpg', '1_500_wb.jpg', True),
    ('1_500.jpg', '1_500_wl.jpg', True),
    ('1_500.jpg', '1_500_sh-100.jpg', True),
    ('1_500.jpg', '1_500_l+100.jpg', True),
    ('1_500.jpg', '1_500_inv.jpg', True),
    ('1_500.jpg', '1_500_brightness.jpg', True),
    ('1_500.jpg', '1_500_brightness-100.jpg', True),
    ('1_500.jpg', '1_500_contrast.jpg', True),

    ('1.jpg', '1.jpg', True),
    ('1.jpg', '1_500.jpg', True),
    ('1.jpg', '1_150.jpg', True),
    ('1.jpg', '2.jpg', False),
    ('1.jpg', '2_500.jpg', False),
    ('1.jpg', '3.jpg', False),
    ('1.jpg', '3_500.jpg', False),
    ('1.jpg', '4.jpg', False),
    ('1.jpg', '4_500.jpg', False),
    ('1.jpg', '5.jpg', False),
    ('1.jpg', '5_500.jpg', False),
    ('1.jpg', '6.jpg', False),
    ('1.jpg', '6_500.jpg', False),
    ('1.jpg', '7.jpg', False),
    ('1.jpg', '7_500.jpg', False),

    ('2.jpg', '1.jpg', False),
    ('2.jpg', '1_500.jpg', False),
    ('2.jpg', '2.jpg', True),
    ('2.jpg', '2_500.jpg', True),
    ('2.jpg', '3.jpg', False),
    ('2.jpg', '3_500.jpg', False),
    ('2.jpg', '4.jpg', False),
    ('2.jpg', '4_500.jpg', False),
    ('2.jpg', '5.jpg', False),
    ('2.jpg', '5_500.jpg', False),
    ('2.jpg', '6.jpg', False),
    ('2.jpg', '6_500.jpg', False),
    ('2.jpg', '7.jpg', False),
    ('2.jpg', '7_500.jpg', False),

    ('3.jpg', '1.jpg', False),
    ('3.jpg', '1_500.jpg', False),
    ('3.jpg', '2.jpg', False),
    ('3.jpg', '2_500.jpg', False),
    ('3.jpg', '3.jpg', True),
    ('3.jpg', '3_500.jpg', True),
    ('3.jpg', '4.jpg', False),
    ('3.jpg', '4_500.jpg', False),
    ('3.jpg', '5.jpg', False),
    ('3.jpg', '5_500.jpg', False),
    ('3.jpg', '6.jpg', False),
    ('3.jpg', '6_500.jpg', False),
    ('3.jpg', '7.jpg', False),
    ('3.jpg', '7_500.jpg', False),

    ('4.jpg', '1.jpg', False),
    ('4.jpg', '1_500.jpg', False),
    ('4.jpg', '2.jpg', False),
    ('4.jpg', '2_500.jpg', False),
    ('4.jpg', '3.jpg', False),
    ('4.jpg', '3_500.jpg', False),
    ('4.jpg', '4.jpg', True),
    ('4.jpg', '4_500.jpg', True),
    ('4.jpg', '5.jpg', False),
    ('4.jpg', '5_500.jpg', False),
    ('4.jpg', '6.jpg', False),
    ('4.jpg', '6_500.jpg', False),
    ('4.jpg', '7.jpg', False),
    ('4.jpg', '7_500.jpg', False),

    ('5.jpg', '1.jpg', False),
    ('5.jpg', '1_500.jpg', False),
    ('5.jpg', '2.jpg', False),
    ('5.jpg', '2_500.jpg', False),
    ('5.jpg', '3.jpg', False),
    ('5.jpg', '3_500.jpg', False),
    ('5.jpg', '4.jpg', False),
    ('5.jpg', '4_500.jpg', False),
    ('5.jpg', '5.jpg', True),
    ('5.jpg', '5_500.jpg', True),
    ('5.jpg', '6.jpg', False),
    ('5.jpg', '6_500.jpg', False),
    ('5.jpg', '7.jpg', False),
    ('5.jpg', '7_500.jpg', False),

    ('6.jpg', '1.jpg', False),
    ('6.jpg', '1_500.jpg', False),
    ('6.jpg', '2.jpg', False),
    ('6.jpg', '2_500.jpg', False),
    ('6.jpg', '3.jpg', False),
    ('6.jpg', '3_500.jpg', False),
    ('6.jpg', '4.jpg', False),
    ('6.jpg', '4_500.jpg', False),
    ('6.jpg', '5.jpg', False),
    ('6.jpg', '5_500.jpg', False),
    ('6.jpg', '6.jpg', True),
    ('6.jpg', '6_500.jpg', True),
    ('6.jpg', '7.jpg', False),
    ('6.jpg', '7_500.jpg', False),

    ('7.jpg', '1.jpg', False),
    ('7.jpg', '1_500.jpg', False),
    ('7.jpg', '2.jpg', False),
    ('7.jpg', '2_500.jpg', False),
    ('7.jpg', '3.jpg', False),
    ('7.jpg', '3_500.jpg', False),
    ('7.jpg', '4.jpg', False),
    ('7.jpg', '4_500.jpg', False),
    ('7.jpg', '5.jpg', False),
    ('7.jpg', '5_500.jpg', False),
    ('7.jpg', '6.jpg', False),
    ('7.jpg', '6_500.jpg', False),
    ('7.jpg', '7.jpg', True),
    ('7.jpg', '7_500.jpg', True),

    ('159.jpg', '160.jpg', True),

    ('madonna.jpg', 'madonna-a.jpg', True),
    ('madonna-a1.jpg', 'madonna-a.jpg', True),
    ('madonna-a2-line.jpg', 'madonna-a.jpg', True),
    ('madonna-sq.jpg', 'madonna-a.jpg', True),
    ('madonna-cropped-face.jpg', 'madonna-a.jpg', True),
    ('madonna-cropped-face2.jpg', 'madonna-a.jpg', True),
    ('madonna-cropped-vertical.jpg', 'madonna-a.jpg', True),

    ('lenna_top.jpg', 'lenna_full.jpg', True),
    ('lenna_face.jpg', 'lenna_full.jpg', True),
    ('lenna_ass.jpg', 'lenna_full.jpg', True),
    ('lenna_cropped.jpg', 'lenna.jpg', True),
)


def test_representative_hash():
    if SKIP_TEST_ALL or SKIP_TEST_REP_HASH:
        assert True
        return

    aspect_ratio = 16 / 9
    # Hash size as (width, height)
    hash_size = [8 * aspect_ratio, 8]
    # Round down width to multiple of 2
    hash_size[0] = int(hash_size[0] - hash_size[0] % 2)

    test_hash = detector.UpNextDetector._generate_initial_hash(*hash_size)  # pylint: disable=protected-access
    detector.UpNextDetector._print_hashes([test_hash], hash_size)  # pylint: disable=protected-access

    test_complete = True
    assert test_complete is True


def test_hash_compare():  # pylint: disable=too-many-locals
    if SKIP_TEST_ALL or SKIP_TEST_HASH_COMPARE:
        assert True
        return

    test_image_path = 'tests/images/'
    match_level = 85
    matches = 0
    false_positives = 0
    false_positives_deviation = 0
    false_negatives = 0
    false_negatives_deviation = 0

    for pairs in IMAGE_PAIRS:
        file1 = pairs[0]
        file2 = pairs[1]
        expected_result = pairs[2]

        try:
            image1 = Image.open(test_image_path + file1)
            image2 = Image.open(test_image_path + file2)
        except (IOError, OSError):
            continue

        aspect_ratio = image1.width / image1.height
        # Hash size as (width, height)
        hash_size = [8 * aspect_ratio, 8]
        # Round down width to multiple of 2
        hash_size[0] = int(hash_size[0] - hash_size[0] % 2)

        hash1, filtered_hash1 = detector.UpNextDetector._create_hashes(  # pylint: disable=protected-access
            image1, image1.size, hash_size
        )
        hash2, filtered_hash2 = detector.UpNextDetector._create_hashes(  # pylint: disable=protected-access
            image2, image2.size, hash_size
        )

        similarity_0 = detector.UpNextDetector._hash_similarity(  # pylint: disable=protected-access
            hash1, hash2
        )
        similarity_1 = detector.UpNextDetector._hash_similarity(  # pylint: disable=protected-access
            hash1, hash2, filtered_hash2
        )
        similarity_2 = detector.UpNextDetector._hash_similarity(  # pylint: disable=protected-access
            hash2, hash1, filtered_hash1
        )
        similarity_3 = detector.UpNextDetector._hash_similarity(  # pylint: disable=protected-access
            filtered_hash1, filtered_hash2
        )
        similarity = max(similarity_0, similarity_1, similarity_2)
        is_match = similarity >= match_level

        if is_match is expected_result:
            matches += 1
        else:
            result_summary = (
                'Comparing: {0} & {1}, '
                'similarity: {2:2.1f}% / {3:2.1f}% / {4:2.1f}% / {5:2.1f}%, '
                'matched: {6}, actual: {7}'
            )
            detector.UpNextDetector._print_hashes(  # pylint: disable=protected-access
                [hash1, hash2, filtered_hash1, filtered_hash2],
                size=hash_size,
                prefix=result_summary.format(
                    file1,
                    file2,
                    similarity_0,
                    similarity_1,
                    similarity_2,
                    similarity_3,
                    is_match,
                    expected_result
                )
            )

        if is_match and not expected_result:
            false_positives += 1
            false_positives_deviation += similarity - match_level
        if not is_match and expected_result:
            false_negatives += 1
            false_negatives_deviation += match_level - similarity

    num_pairs = len(IMAGE_PAIRS)
    percent_matched_correctly = 100 * matches / len(IMAGE_PAIRS)
    if false_negatives:
        false_negatives_deviation /= false_negatives
    if false_positives:
        false_positives_deviation /= false_positives
    results_summary = (
        'Correct matches: {0}/{1} ({2:2.1f}%),'
        '{3} false positives (mean deviation: {4}),'
        '{5} false negatives (mean deviation: {6})'
    )
    print(results_summary.format(
        matches,
        num_pairs,
        percent_matched_correctly,
        false_positives,
        false_positives_deviation,
        false_negatives,
        false_negatives_deviation
    ))
    assert percent_matched_correctly >= 90
