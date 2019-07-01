from typing import List # for type annotation

# Function which converts a unit numeral to a textual number
def unit_to_text(number: int) -> str:
    # TODO use a dictionary implementation rather than an if-else tree
    # dictionaries would ideally be decalred first thing in the normalise_sentence function
    # for improved efficiency
    if number == 0:
        return "żero"
    elif number == 1:
        return "wieħed"
    elif number == 2:
        return "tnejn"
    elif number == 3:
        return "tlieta"
    elif number == 4:
        return "erbgħa"
    elif number == 5:
        return "ħamsa"
    elif number == 6:
        return "sitta"
    elif number == 7:
        return "sebgħa"
    elif number == 8:
        return "tmienja"
    elif number == 9:
        return "disgħa"


# Function which converts a tenth numeral to a textual number
def tenth_to_text(number: int) -> str:
    if number == 10:
        return "għaxra"
    elif number == 11:
        return "ħdax"
    elif number == 12:
        return "tnax"
    elif number == 13:
        return "tlettax"
    elif number == 14:
        return "erbatax"
    elif number == 15:
        return "ħmistax"
    elif number == 16:
        return "sittax"
    elif number == 17:
        return "sbatax"
    elif number == 18:
        return "tmintax"
    elif number == 19:
        return "dsatax"
    elif number == 20:
        return "għoxrin"
    elif number == 30:
        return "tletin"
    elif number == 40:
        return "erbgħin"
    elif number == 50:
        return "ħamsin"
    elif number == 60:
        return "sittin"
    elif number == 70:
        return "sebgħin"
    elif number == 80:
        return "tmenin"
    elif number == 90:
        return "disgħin"


def hundredth_to_text(number: int) -> str:
    if number == 100:
        return "mija"
    elif number == 200:
        return "mitejn"
    elif number == 300:
        return "tliet mija"
    elif number == 400:
        return "erba' mija"
    elif number == 500:
        return "ħames mija"
    elif number == 600:
        return "sitt mija"
    elif number == 700:
        return "seba' mija"
    elif number == 800:
        return "tminn mija"
    elif number == 900:
        return "disa' mija"


def thousandth_to_text(number: int) -> str:
    if number == 1000:
        return "elf"
    elif number == 2000:
        return "elfejn"
    elif number == 3000:
        return "tlett elef"
    elif number == 4000:
        return "erbat elef"
    elif number == 5000:
        return "ħamest elef"
    elif number == 6000:
        return "sitt elef"
    elif number == 7000:
        return "sebat elef"
    elif number == 8000:
        return "tmint elef"
    elif number == 9000:
        return "disat elef"


def normalise_integer_token(token: str) -> str:
    number: int = int(token)
    normalised_text: str = ""

    if 0 <= number <= 9:
        normalised_text = unit_to_text(number)
    elif 10 <= number <= 99:
        unit: int = int(str(number)[-1])
        tenth: int = int(str(number)[-2]) * 10
        if number <= 19:
            normalised_text = tenth_to_text(number)
        elif unit == 0:
            normalised_text = tenth_to_text(number)
        else:
            normalised_text = normalise_integer_token(unit) + ' u ' + tenth_to_text(tenth)
    elif 100 <= number <= 999:
        unit: int = int(str(number)[-1])
        tenth: int = int(str(number)[-2]) * 10
        hundredth: int = int(str(number)[-3]) * 100

        if unit == 0:
            return hundredth_to_text(hundredth) + ' u ' + tenth_to_text(tenth)
        else:
            return hundredth_to_text(hundredth) + ' ' + normalise_integer_token(number - hundredth)
    elif 1000 <= number <= 9999:
        unit: int = int(str(number)[-1])
        tenth: int = int(str(number)[-2]) * 10
        hundredth: int = int(str(number)[-3]) * 100
        thousandth: int = int(str(number)[-4]) * 1000

        return thousandth_to_text(thousandth) + ' ' + normalise_integer_token(number - thousandth)

    return normalised_text


# Function which normalises a list of tokens to regular text
def normalise_sentence(sentence: List[str]) -> List[str]:
    normalised_sentence: List[str] = list()

    # iterating over all the tokens in the sentence
    for token in sentence:
        # checking if the token is an integer
        if token.isdigit():
            normalised_token = normalise_integer_token(token)
        # TODO handling of further NSWs can be added here
        # Real numbers, Dates, Measurements, Abbreviations etc

        # if the token is regular text
        else:
            normalised_token = token

        # append the normalised text to the normalised_sentence list (of text)
        normalised_sentence.append(normalised_token)

    return normalised_sentence


if __name__ == '__main__':
    sentence: List[str] = ['Jien', 'ghandi', '0', '9', '33', '30', '123', '4567', '9999',
                           '10000', '9,999', '-1', '9.0', '25!', '50cm']
    # out of range, negative, decimal point, with punctuation, symbols
    # dates, abbreviations,
    print(sentence)
    print(normalise_sentence(sentence))