raw = """
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import advent\\n",
    "advent.scrape(2015, DAYNR)\\n",
    "data = advent.get_lines(DAYNR)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": ".venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.10.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
"""
for i in range(1, 26):
    content = raw.replace("DAYNR", str(i))
    with open(f'advent{i}.ipynb', 'w') as f:
        f.write(content)