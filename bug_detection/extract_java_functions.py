import re

def extract_functions_from_java_class(java_code):
    """
    Extracts functions from a Java class and returns a dictionary 
    with function names as keys and their signatures and bodies combined as values.

    :param java_code: str, the complete Java class code
    :return: dict, a dictionary of functions and their content combined
    """
    # Regular expression to match Java methods (start of function)
    method_pattern = re.compile(
        r'(?P<visibility>public|protected|private|static)?\s*(?P<return_type>\w[\w\s<>[\]]*)\s+(?P<name>\w+)\s*\((?P<params>[^)]*)\)\s*{',
        re.DOTALL
    )

    functions = {}
    
    # Finding all methods and their locations
    for match in method_pattern.finditer(java_code):
        start_index = match.start()
        visibility = match.group('visibility') or ''
        return_type = match.group('return_type').strip()
        name = match.group('name')
        params = match.group('params').strip()

        # Start looking for the closing brace
        body_start = match.end()
        brace_count = 1  # We have found an opening brace

        # Find the closing brace
        for i in range(body_start, len(java_code)):
            if java_code[i] == '{':
                brace_count += 1
            elif java_code[i] == '}':
                brace_count -= 1
            
            # If brace count is zero, we've found the closing brace
            if brace_count == 0:
                body = java_code[body_start:i].strip()
                combined = f"{visibility} {return_type} {name}({params}) {{\n{body}\n}}"
                functions[name] = combined  # Use function name as key, combined as value
                break
    
    return functions

# Example Java class code
java_class_code = """
public class TrickyLogic {
    public int index;
    private final String separator = File.separator;

    public static void runForever() {
        while (true) {
            System.out.println("Running forever...");
        }
    }

    public void non_buggy_loop() throws IOException {
        try (IndexReader ireader = IndexReader.open(indexDirectory);
             TermEnum iter = ireader.terms(new Term("u", ""))) {
            while (iter.term() != null) {
                log.info(Util.uid2url(iter.term().text()));
                iter.next();
            }
        } catch (Exception e) {
            log.error("Error closing index resources", e);
        }
    }

    public void getNextEditor() {
        EditorPartPresenter nextPart = null;
        Iterator<EditorPartPresenter> iterator = openedEditors.values().iterator();
        while (iterator.hasNext()) {
            EditorPartPresenter editor = iterator.next();
            if (activeEditor.equals(editor) && iterator.hasNext()) {
                nextPart = iterator.next();
                break;
            }
        }
        return nextPart;
    }

    public void infiniteLoop() {
        EditorPartPresenter nextPart = null;
        Iterator<EditorPartPresenter> iterator = Iterators.cycle(openedEditors.values());
        while (true) {
            EditorPartPresenter editor = iterator.next();
            if (activeEditor.equals(editor) && iterator.hasNext()) {
                nextPart = iterator.next();
            }
        }
    }

    public String extractFolder(String path) {
        String result = "";
        int index = path.lastIndexOf(separator);
        result = path.substring(0, index);
        return result;
    }
}
"""

