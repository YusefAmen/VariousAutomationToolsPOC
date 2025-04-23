"""
You are given a 2D integer array items where each entry [price_i, profit_i] represent price and profit of an item
respectively.
You are given a 0-indexed integer array budgets containing budget points to evaluate. 
For each amount in budgets, you want to find the maximum profit of an item whose price is less than or equal to the
current budget.
If no such item exists, return 0.
Example 1:
Input:
items = [[1, 2], [3, 2], [2, 4], [5, 6], [3, 5]]
budgets = [1, 2, 3, 4, 5, 6]
Output: [2, 4, 5, 5, 6, 6]
Explanation:
For budgets[0]=1, [1,2] is the only item which has price <= 1. Hence, the answer for this price is 2.
- For budgets[1]=2, the items which can be considered are [1,2] and [2,4]. 
  The maximum profit among them is 4.
- For budgets[2]=3 and budgets[3]=4, the items which can be considered are [1,2], [3,2], [2,4], and [3,5].
  The maximum profit among them is 5.
- For budgets[4]=5 and budgets[5]=6, all items can be considered.
  Hence, the answer for them is the maximum profit of all items, i.e., 6.
Example 2:
Input: items = [[1,2],[1,2],[1,3],[1,4]], budgets = [1]
Output: [4]
"""
from typing import List

class Solution:
    def maximumProfit(self, items: List[List[int]], budgets: List[int]) -> List[int]:
        # Your implementation


        # items = [[1, 2], [3, 2], [2, 4], [5, 6], [3, 5], [2, 9]]
        # budgets = [1, 2, 3, 4, 5, 6]

        #  hashmap = {1: 2, 2: 9, ...}
        # OPTIMIZED O(N)
        hashmap = {}
        for item in items:
            if item[0] in hashmap:
                if item[1] > hashmap[item[0]]:
                    hashmap[item[0]] = item[1]
            else:
                hashmap[item[0]] = item[1]

        budget_matching = []
        for budget in budgets:
            budget_matching.append(hashmap[budget])


        return budget_matching


        # NOT OPTIMAL
        # O(NK) 
        budget_matching = []
        for budget in budgets:
            maximum_so_far = 0
            for item in items:
                if budget >= item[0]:
                    if maximum_so_far < item[1]:
                        maximum_so_far = item[1]

            budget_matching.append(maximum_so_far)

        return budget_matching

