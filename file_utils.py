from typing import List, Sequence, Callable, Tuple, Dict, Set
import os
import re
import subprocess
import csv


def save_in_text(output_file: str, values: List[str]):
    with open(output_file, "w", encoding="utf-8") as f:
        for value in values:
            f.write(value)
            f.write("\n")
    
    
def search_original_path(name: str, list_of_values: List[str]) -> List[str]:
    return list(filter(lambda x: name in x, list_of_values))


def open_path(path: str, open_dir=False):
    if open_dir:
        path = os.path.dirname(path)
    subprocess.Popen(f"explorer {path}")
    
    
def search_regex(regex: str, files: List[str], split_result=False, skip_empty=True) -> Sequence:
    regex = re.compile(regex)
    result = set()
    for file in files:
        matchs = regex.findall(file)
        if skip_empty and not matchs:
            continue
        if split_result:
            result.update(matchs)
        else:
            result.add(" ".join(matchs))
    return result


def run_filter_pipeline(elements: List["str"], pipelines_filter: List[Callable]) -> List[str]:
    for pipeline in pipelines_filter:
        elements = filter(pipeline, elements)
    return list(elements)


def run_replacement(elements: List["str"], replacements: Tuple[Tuple[str, str]], use_regex=False, count=0) -> List[str]:
    """ Make a replacement in all values in elements.
    The format of tuple of replacement is (pattern, replace)
    
    """
    results = elements[:]
    for pattern, replace in replacements:
        if use_regex:
            regex = re.compile(pattern)
            
        for i in range(len(results)):
            if use_regex:
                results[i] = regex.sub(replace, results[i], count=count)
            else:
                results[i] = results[i].replace(pattern, replace)
            
    return results


def filter_file_with_regex(regex: str, files: List[str]) -> List[str]:
    regex = re.compile(regex)
    return [
        file for file in files if regex.search(file)
    ]


def exclude_file_with_regex(regex: str, files: List[str]) -> List[str]:
    regex = re.compile(regex)
    return [
        file for file in files if not regex.search(file)
    ]


def save_in_csv(output_file: str, headers: List[str], data: List[Dict]):
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


def load_csv(filename: str, class_object: Callable) -> List[object]:
    results = []
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(class_object(**row))
    return results


def exclude_paths_in_exclude_list(filename: str, excluded_paths: Set[str]):
    for excluded_path in excluded_paths:
        if excluded_path in filename:
            return False
    return True
