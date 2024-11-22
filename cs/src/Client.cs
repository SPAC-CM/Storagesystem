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
                    await CreateProduckt(client, "Top hat", 13.2f, 2);

                    //GET request
                    await ReadProductDatabase(client);


                }
                catch (HttpRequestException e)
                {
                    Console.WriteLine($"An error occurred while making the request: {e.Message}");
                }
            }
        }
        public async Task CreateProduckt(HttpClient client, string ProductName, float Price, int StockQuantity)
        {
            try
            {
                var dataPackage = new
                {
                    ProductName, Price, StockQuantity
                };

                // Convert the object to JSON string
                var jsonContent = JsonSerializer.Serialize(dataPackage);
                //Post Request
                HttpResponseMessage response = await client.PostAsync(URL, new StringContent(jsonContent, System.Text.Encoding.UTF8, "application/json"));
                if(response.IsSuccessStatusCode)
                {
                    System.Console.WriteLine("Made product");
                }
                else
                    System.Console.WriteLine($"Error: {response.StatusCode}");
            }
            catch (System.Exception e)
            {
                System.Console.WriteLine(e);
                throw;
            }
        }

        public async Task ReadProductDatabase(HttpClient client)
        {
            HttpResponseMessage response = await client.GetAsync(URL);

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
                Console.WriteLine($"Error in ReadProductDatabase: {response.StatusCode}");
            }
        }
        
    }
}
