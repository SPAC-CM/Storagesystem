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
                    //Read
                    await ReadProductByName(client, "Test");

                    await UpdateProductDatabase(client, 2, "Truck", 5.2f, 4);
                    /*  
                    //CREATE request
                    await CreateProduckt(client, "Top hat", 13.2f, 2);

                    //GET hole table
                    await ReadProductDatabase(client);
                    */

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
                    System.Console.WriteLine(response);
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

        public async Task ReadProductByID(HttpClient client, int targetID)
        {
            try
            {
                string targetURL = $"{URL}_item_id?id={targetID}";

                HttpResponseMessage response = await client.GetAsync(targetURL);

                if(response.IsSuccessStatusCode) 
                {
                    string content = await response.Content.ReadAsStringAsync();
                    System.Console.WriteLine(content);
                }
            }
            catch (System.Exception e)
            {
                System.Console.WriteLine(e);
            }
        }

        public async Task ReadProductByName(HttpClient client, string name)
        {
            try
            {
                string targetURL = $"{URL}_item_name?name={name}";

                HttpResponseMessage response = await client.GetAsync(targetURL);

                if(response.IsSuccessStatusCode)
                {
                    string content = await response.Content.ReadAsStringAsync();
                    System.Console.WriteLine(content);
                }
            }
            catch (System.Exception e)
            {
                System.Console.WriteLine(e);
            }
        }

        public async Task UpdateProductDatabase(HttpClient client, int targetID, 
            string updatedName = "", float updatedPrice = 0, int updateStock = 0)
        {
            try
            {
            // Prepare the request body as JSON
                var content = new
                {
                    name = updatedName,
                    price = updatedPrice,
                    stock = updateStock
                };

                // Convert the content to JSON string
                string jsonContent = JsonSerializer.Serialize(content);

                // Create a StringContent object with the JSON content
                using (StringContent requestBody = new StringContent(jsonContent, System.Text.Encoding.UTF8, "application/json"))
                {
                    // Prepare the PUT request
                    HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Put, $"{URL}_update_id?id={targetID}");

                    // Add the request body
                    request.Content = requestBody;

                    HttpResponseMessage response = await client.SendAsync(request);

                    if(response.IsSuccessStatusCode)
                    {
                        System.Console.WriteLine("Updated item");
                    }
                    else
                    {
                        System.Console.WriteLine($"Error: {response.StatusCode}");
                    }
                }
            }
            catch (System.Exception e)
            {
                System.Console.WriteLine(e);
            }
        }
    }
}