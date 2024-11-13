//using MySql.Data.MySqlClient;
//public sealed class SQLManager
//{
//	private static readonly SQLManager instance = new SQLManager();
//	
//	private MySqlConnection? connector;
//
//	private SQLManager()
//	{
//	}
//	
//	static SQLManager()
//	{
//	}
//
//	public static SQLManager Instance { get {return instance;}}
//
//	public void set_connection(string user, string password, string database)
//	{
//		try
//		{	
//			connector = new MySqlConnection("server=127.0.0.1;uid="+ user +";pwd="+ password +";database=" + database);
//			connector.Open();
//
//		}
//		catch (MySqlException ex)
//		{
//			System.Console.WriteLine(ex.Message);
//		}
//	}
//
//	public void insert()
//	{
//		if(connector is not null)
//		{
//			string query = "INSERT INTO Catagories(CatagoryName) Values('Stuffs')";
//			MySqlCommand command = new MySqlCommand(query,connector);
//			command.ExecuteNonQuery();
//		}
//
//	}
//}
