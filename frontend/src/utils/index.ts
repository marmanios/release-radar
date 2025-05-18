export const getIconPathForSource = (source: string) => {
    switch (source) {
        case "python":
            return "/source_icons/python.svg";
        case "github":
            return ""
        
        default:
            return "/question-mark.svg";        
    }
}
