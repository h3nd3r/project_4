import json

def find_all_json(text):
    def find_matching_bracket(s, start, open_char, close_char):
        stack = []
        for i in range(start, len(s)):
            if s[i] == open_char:
                stack.append(open_char)
            elif s[i] == close_char:
                if not stack:
                    return -1
                stack.pop()
                if not stack:
                    return i
        return -1

    json_objects = []
    i = 0
    while i < len(text):
        # Find the start of a potential JSON object or array
        start = text.find('{', i)
        array_start = text.find('[', i)
        if start == -1 and array_start == -1:
            break
        if (array_start != -1 and array_start < start) or start == -1:
            start = array_start
            end = find_matching_bracket(text, start, '[', ']')
        else:
            end = find_matching_bracket(text, start, '{', '}')
        
        if end == -1:
            i = start + 1
            continue

        # Try to parse the potential JSON
        try:
            json_obj = json.loads(text[start:end+1])
            json_objects.append(json_obj)
        except json.JSONDecodeError:
            pass
        
        i = end + 1

    return json_objects