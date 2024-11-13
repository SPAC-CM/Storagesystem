using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Net.Http;
using System.Text.Json;

namespace cs.src
{
    public class Client
    {
        public async Task Connect()
        {
            using (var client = new HttpClient())
            {
                // Set the base address for the API
                client.BaseAddress = new Uri("http://localhost:5000");

                try
                {
                    // Make a GET request to the API endpoint
                    HttpResponseMessage response = await client.GetAsync("/products");

                    if (response.IsSuccessStatusCode)
                    {
                        // Parse the JSON response
                        string jsonResponse = await response.Content.ReadAsStringAsync();
                        JsonDocument jsonDoc = JsonDocument.Parse(jsonResponse);

                        // Process the JSON data
                        Console.WriteLine($"API Response: {jsonDoc.RootElement}");
                    }
                    else
                    {
                        Console.WriteLine($"Error: {response.StatusCode}");
                    }
                }
                catch (HttpRequestException e)
                {
                    Console.WriteLine($"An error occurred while making the request: {e.Message}");
                }
            }
        }
    }
}