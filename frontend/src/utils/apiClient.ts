const makeApiRequest = async (
    endpoint: string,
    method: 'GET' | 'POST' = 'POST',
    body?: Record<string, any>
  ): Promise<any> => {
    const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    });
  
    if (!response.ok) {
      let errorDetail = `HTTP error! Status: ${response.status}`;
  
      try {
        const errorBody = await response.json();
        if (errorBody?.detail) {
          errorDetail = errorBody.detail;
        }
      } catch (_) {
        // JSON parsing failed — keep default errorDetail
      }
  
      // Throw an error object with the `detail` property
      const error = new Error(errorDetail);
      (error as any).detail = errorDetail;
      throw error;
    }
  
    return response.json();
  };

export default makeApiRequest