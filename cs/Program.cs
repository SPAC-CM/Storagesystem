using System;
using System.Threading.Tasks;
using cs.src;

class Program
{
    static async Task Main(string[] args)
    {
        try
        {
            Client client = new Client();
            await client.Connect();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
    }
}