const API_BASE_URL = 
    import.meta.env.VITE_API_BASE_URL ?? "/api";

export class ApiError extends Error {
    public readonly status: number;

    constructor(status: number, message: string) {
        super(message)
        
        this.name = "ApiError";
        this.status = status;
    }
} 

export async function apiGet<T>(
    endpoint: string,
    signal?: AbortSignal 

): Promise<T> {
    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
         { signal }
    );

    if (!response.ok) {
        throw new ApiError(
            response.status,
            `API request failed: ${response.status}`
        );
    }

    return (await response.json()) as T;
}