string connectionString = "server=localhost;port=3305;database=parking;uid=root";

using (MySqlConnection connection = new MySqlConnection(connectionString))
{
// Create database if not exists
using (Parking contextDB = new Parking(connection, false))
{
  contextDB.Database.CreateIfNotExists();
}

connection.Open();
MySqlTransaction transaction = connection.BeginTransaction();

try
{
  // DbConnection that is already opened
  using (Parking context = new Parking(connection, false))
  {

    // Interception/SQL logging
    context.Database.Log = (string message) => { Console.WriteLine(message); };

    // Passing an existing transaction to the context
    context.Database.UseTransaction(transaction);

    // DbSet.AddRange
    List<Car> cars = new List<Car>();

    cars.Add(new Car { Manufacturer = "Nissan", Model = "370Z", Year = 2012 });
    cars.Add(new Car { Manufacturer = "Ford", Model = "Mustang", Year = 2013 });
    cars.Add(new Car { Manufacturer = "Chevrolet", Model = "Camaro", Year = 2012 });
    cars.Add(new Car { Manufacturer = "Dodge", Model = "Charger", Year = 2013 });

    context.Cars.AddRange(cars);

    context.SaveChanges();
  }

  transaction.Commit();
}
catch
{
  transaction.Rollback();
  throw;
}
}
