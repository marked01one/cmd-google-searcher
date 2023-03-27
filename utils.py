from email.quoprimime import body_check
import requests
from bs4 import BeautifulSoup


class BadRequest(Exception):
  """
  Utility exception to handle bad requests
  """


class InternalServerError(Exception):
  """
  Utility exception to handle internal server errors
  """


class NotEnoughArgumentsError(Exception):
  '''
  Utility class that raises error when there are not enough exceptions
  '''


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class SearchScraper:
  def __init__(self, search_string: str) -> None:
    self.search_string = search_string
    self.url_list: list[str] = []
    self.content_list: list[dict] = []
    
    # Prepare the search string & make request
    prep = self.search_string.replace(" ", "+")
    self.response = requests.get(f"https://www.google.com/search?q={prep}&sourceid=chrome&ie=UTF-8")
    # Check for HTTP errors
    self._check_errors()
    # Print to console the success message
    print(f"\n{bcolors.OKBLUE}Status code {self.response.status_code} - Search was successful{bcolors.ENDC}")
  

  def get_urls(self) -> None:
    '''
    Get all urls contained within the requested Google search
    '''
    soup = BeautifulSoup(self.response.content, "html.parser")
    for link in soup.find_all('a'):
      url = link.get('href')
      
      if url[:5] == '/url?' and 'google' not in url:
        self.url_list.append(url[7:].split("&")[0]) 
    return
  
  
  def get_content_in_urls(self) -> None:
    for url in self.url_list:
      self.content_extractor(url)


  def content_extractor(self, url) -> None:
    res = requests.get(url)
    out_dict: dict = {}
    try:
      self._check_errors(status=res.status_code)
    except BadRequest or InternalServerError:
      self.content_list.append({"Error": f"{bcolors.FAIL}Content for website '{bcolors.UNDERLINE}{url}{bcolors.ENDC}{bcolors.FAIL}' is not accesible{bcolors.ENDC}"})
    else:
      soup = BeautifulSoup(res.content, "html.parser")
      out_dict["website_title"] = (bcolors.HEADER + soup.title.string + bcolors.ENDC) if (soup.title != None) else "No title was found"
      for mt in soup('meta'):
        try:
          if mt['name'] == 'description':
            out_dict["description"] = bcolors.OKGREEN + mt['content'] + bcolors.ENDC
            break
        except KeyError:
          pass
      
      out_dict["url"] = f"{bcolors.BOLD}URL:{bcolors.ENDC} {bcolors.UNDERLINE}{url}{bcolors.ENDC}"
      # Add content of website to list
      self.content_list.append(out_dict)
    return
  
  def print_content(self) -> None:
    for content in self.content_list:
      output = "\n"
      for key in content.values():
        output += f"{key}\n"
      
      print(output)
    return
  
  # ! Private method: not meant for use outside of class
  def _check_errors(self, status: int = None):
    if not status:
      if self.response.status_code // 100 == 4:
        raise BadRequest(f"Error code {self.response.status_code} - Request was not successful due to client restrictions")
      if self.response.status_code // 100 == 5:
        raise InternalServerError(f"Error code {self.response.status_code} - Request was not successful due to server error")
      return
    
    else:
      if status // 100 == 4:
        raise BadRequest(f"Error code {self.response.status_code} - Request was not successful due to client restrictions")
      if status // 100 == 5:
        raise InternalServerError(f"Error code {self.response.status_code} - Request was not successful due to server error")
      return