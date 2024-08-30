export type EnumTextChoice = {label: string, value: string}

export type EnumTextChoices = Record<string, EnumTextChoice>

export const EnumAccountTypes: EnumTextChoices =  {
  'staff': {
    label: "Staff",
    value: "staff"
  },
  'user': {
    label: "User",
    value: "user"
  }
}

export const EnumTokenAddresses: EnumTextChoices =  {
  '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599': {
    label: "Wbtc",
    value: "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
  },
  '0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce': {
    label: "Shib",
    value: "0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce"
  },
  '0x6810e776880c02933d47db1b9fc05908e5386b96': {
    label: "Gno",
    value: "0x6810e776880c02933d47db1b9fc05908e5386b96"
  }
}