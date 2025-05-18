export type TApiResponse<t> = { 
    data: t | null, 
    message: string 
};

export type TAiSummary = {
    "summary": string;
    "notes": string[];
    "supplementary_definitions": {term: string, definition: string}[];
}