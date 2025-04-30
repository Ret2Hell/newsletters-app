import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { BaseQueryApi, FetchArgs } from "@reduxjs/toolkit/query";
import { toast } from "sonner";

const customBaseQuery = async (
  args: string | FetchArgs,
  api: BaseQueryApi,
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  extraOptions: any
) => {
  const baseQuery = fetchBaseQuery({
    baseUrl: process.env.NEXT_PUBLIC_BASE_URL,
  });
  try {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const result: any = await baseQuery(args, api, extraOptions);

    if (result.error) {
      const errorData = result.error.data;
      const errorMessage =
        errorData?.message ||
        result.error.status.toString() ||
        "An error occurred";
      toast.error(`${errorMessage}`);
    }

    const isMutationRequest =
      (args as FetchArgs).method && (args as FetchArgs).method !== "GET";
    if (isMutationRequest) {
      const successMessage = result.data?.message;
      if (successMessage) {
        toast.success(successMessage);
      }
    }

    if (result.data) {
      result.data = result.data.data;
    } else if (
      result.error?.status === 204 ||
      result.meta?.response?.status === 24
    ) {
      return { data: null };
    }
    if (result.data === undefined && result.error === undefined) {
      return { data: null };
    }
    return result;
  } catch (error: unknown) {
    const errorMessage =
      error instanceof Error ? error.message : "Unknown error";

    return { error: { status: "FETCH_ERROR", error: errorMessage } };
  }
};

export const api = createApi({
  baseQuery: customBaseQuery,
  reducerPath: "api",
  tagTypes: ["Newsletter"],
  endpoints: (builder) => ({
    generateContent: builder.mutation({
      query: (body: { prompt: string }) => ({
        url: "/newsletters/generate",
        method: "POST",
        body,
      }),
    }),
    createNewsletter: builder.mutation({
      query: (body: {
        prompt: string;
        generated_content: string;
        edited_content: string;
      }) => ({
        url: "/newsletters",
        method: "POST",
        body,
      }),
      invalidatesTags: ["Newsletter"],
    }),
    getNewsletters: builder.query({
      query: ({
        skip = 0,
        limit = 10,
      }: { skip?: number; limit?: number } = {}) => ({
        url: "/newsletters",
        params: { skip, limit },
      }),
      providesTags: ["Newsletter"],
    }),
    getNewsletter: builder.query({
      query: (id: string) => `/${id}`,
      providesTags: (result, error, id) => [{ type: "Newsletter", id }],
    }),
    updateNewsletter: builder.mutation({
      query: ({
        id,
        edited_content,
      }: {
        id: string;
        edited_content: string;
      }) => ({
        url: `/newsletters/${id}`,
        method: "PATCH",
        body: { edited_content },
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "Newsletter", id }],
    }),
    deleteNewsletter: builder.mutation({
      query: (id: string) => ({
        url: `/newsletters/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: (result, error, id) => [{ type: "Newsletter", id }],
    }),
  }),
});

export const {
  useGenerateContentMutation,
  useCreateNewsletterMutation,
  useGetNewslettersQuery,
  useGetNewsletterQuery,
  useUpdateNewsletterMutation,
  useDeleteNewsletterMutation,
} = api;
