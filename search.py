from utils import SearchScraper, NotEnoughArgumentsError, bcolors
import sys


if len(sys.argv) == 1:
  raise NotEnoughArgumentsError("Must include a search string")

search_string = " ".join(sys.argv[1:])
scraper = SearchScraper(search_string=search_string)
print(f"{bcolors.WARNING}{bcolors.BOLD}SEARCH STRING: '{search_string}'{bcolors.ENDC}")

scraper.get_urls()
scraper.get_content_in_urls()
scraper.print_content()

