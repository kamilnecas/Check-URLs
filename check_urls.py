import requests
import re


def split_merged_urls(urls_p, regex_p):
    """
    It searches for merged URLs and splits them. It splits merged URLs via regular expression.
    This is to prevent cases when URLs are not separated by line break.
    :param urls_p: List of URLs.
    :param regex_p: Regular expression is provided/written in method 'perform_split_merged_urls'.
    """

    for index, url in enumerate(urls_p):
        merged_url = re.search(regex_p, url)

        if merged_url:
            # Removing (replacing) URL from same list item.
            urls_p[index] = urls_p[index].replace(merged_url[0], '')
            # Adding removed (replaced) URL to the list.
            urls_p.append(merged_url[0])


def perform_split_merged_urls(urls_p):
    """
    It performs splitting of merged URLs. It calls method 'split_merged_urls'.
    :param urls_p: List of URLs.
    """

    # Negative lookbehind searches for URLs which are not located at the beginning of the line.
    split_merged_urls(urls_p, r'(?<!^)(https://.*)$')
    split_merged_urls(urls_p, r'(?<!^)(http://.*)$')
    split_merged_urls(urls_p, r'(?<!^)(?<!https://)(?<!http://)(www\..*)$')


def check_add_schema(urls_p):
    """
    It check URLs via regular expression, if it has schema (http protocol).
    If not, schema is added to particular URL at the beginning.
    :param urls_p: List of URLs.
    """

    for index, url in enumerate(urls_p):
        if not re.match(r'http[s]?://', url):
            urls_p[index] = 'http://' + urls_p[index]


def load_urls():
    """
    It loads URLs and validates them for status check.
    Validation includes splitting merged URls, checking/adding schema, stripping leading/trailing spaces
    and removing duplicates.
    Input URLs have to be stored in txt file 'urls_input.txt'. Txt file is created by user.
    Methods 'perform_split_merged_urls' and 'check_add_schema' are called.
    :return: List of URLs or empty list.
    """

    try:
        file_txt_in = open('urls_input.txt', 'r', encoding='UTF-8')

        urls = file_txt_in.read().splitlines()

        if len(urls) > 0:
            # This allows us to ignore \n symbol at the end of the line.
            # If we use readlines(), it will include the \n symbol.

            # Using list comprehension to remove empty lines.
            urls = [line for line in urls if line]

            perform_split_merged_urls(urls)
            check_add_schema(urls)

            # Using list comprehension to remove trailing spaces.
            # The if condition checks if line is not empty.
            urls = [url.strip() for url in urls]

            # Removing duplicates.
            urls = list(dict.fromkeys(urls))

            file_txt_in.close()
            return urls
        else:
            print('Input file is empty.')
            file_txt_in.close()
            return []

    except FileNotFoundError:
        print('Input file not found.')
        return []


def check_status_of_url(request_p, accessible_urls_p, non_accessible_urls_p):
    """
    It checks, if provided URL returns (http) status code 200.
    Based on result, URL is added to either 'accessible_urls_p' list or 'non_accessible_urls_p' list.
    :param request_p: Provided URL.
    :param accessible_urls_p: List of accessible URLs.
    :param non_accessible_urls_p: List of non-accessible URLs.
    """

    if request_p.status_code == 200:
        # Adding accessible URL into extra list.
        accessible_urls_p.append(request_p.url)
    else:
        # Adding non-accessible URL into extra list.
        non_accessible_urls_p.append(request_p.url)


def check_status_of_urls(load_urls_p):
    """
    It checks status code for loaded URLs by calling the method 'check_status_of_url'.
    :param load_urls_p: It stores list of validated URLs for status check.
    :return: List of accessible URLs and list non-accessible URLs or 2 empty lists.
    """

    accessible_urls = []
    non_accessible_urls = []

    if len(load_urls_p) > 0:

        for url_link in load_urls_p:

            try:
                request = requests.get(url_link)
                check_status_of_url(request, accessible_urls, non_accessible_urls)

            except Exception:
                non_accessible_urls.append(url_link)

        # Sort can be useful as same as frustrating in some cases. Not used.
        # accessible_urls.sort()
        # non_accessible_urls.sort()

        return accessible_urls, non_accessible_urls

    else:
        return [], []


def save_urls_report():
    """
    It creates summary report of accessible and non-accessible URLs.
    Report is saved as txt file 'urls_output.txt'. Txt file is created in same directory as Python script.
    Report contains validated overview of URLs for both categories and their total counts.
    """

    loaded_urls = load_urls()

    if len(loaded_urls) > 0:

        file_txt_out = open('urls_output.txt', 'w', encoding='UTF-8')

        file_txt_out.write('Accessible URLs: ' + str(len(check_status_of_urls(loaded_urls)[0])) + '\n')

        for url in check_status_of_urls(loaded_urls)[0]:
            file_txt_out.write('|- ' + url + '\n')

        file_txt_out.write('Non-accessible URLs: ' + str(len(check_status_of_urls(loaded_urls)[1])) + '\n')

        for url in check_status_of_urls(loaded_urls)[1]:
            file_txt_out.write('|- ' + url + '\n')

        file_txt_out.close()

        print('Done. Please, check the result in "urls_output.txt".')


if __name__ == '__main__':

    save_urls_report()

