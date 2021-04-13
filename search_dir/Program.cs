using System;
using System.Collections.Generic;

class Program {

        static void Main(string[] args)
        {
            var link = "http://www.litra.ru/composition";
            var search = new Search(link);

            search.SearchWord("сочинение по произведениям андерсена");

            Console.WriteLine();
        }
}