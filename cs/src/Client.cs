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
        string targetPort = "http://localhost:5000";
        string URL = "/products";

        public async Task Connect()
        {
            using (var client = new HttpClient())
            {
                // Set the base address for the API
                client.BaseAddress = new Uri(targetPort);

                try
                {
                    //CREATE request
                    // Create a new product
                    var newProduct = new
                    {
                        ProductName = "Create hat",
                        Price = 20,
                        StockQuantity = 1
                    };

                    // Convert the object to JSON string
                    var jsonContent = JsonSerializer.Serialize(newProduct);

                    //Post Request
                    HttpResponseMessage response = await client.PostAsync(URL, new StringContent(jsonContent, System.Text.Encoding.UTF8, "application/json"));

                    if(response.IsSuccessStatusCode)
                    {
                        System.Console.WriteLine("Made product");
                    }
                    else
                        System.Console.WriteLine($"Error: {response.StatusCode}");

                    /*
                    //CREATE request with 2 parametors
                    // Create a new product
                    var nextProduct = new
                    {
                        name = "T-shirt",
                        categori = "Spring"
                    };

                    // Convert the object to JSON string
                    jsonContent = JsonSerializer.Serialize(nextProduct);

                    //Post Request
                    response = await client.PostAsync(URL, new StringContent(jsonContent, System.Text.Encoding.UTF8, "application/json"));

                    if(response.IsSuccessStatusCode)
                    {
                        
                    }
                    else
                        System.Console.WriteLine($"Error: {response.StatusCode}");
                    */
                    
                    //GET request
                    response = await client.GetAsync(URL);

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
                        System.Console.WriteLine();
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